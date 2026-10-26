# -*- coding: utf-8 -*-
# T12_ATRATOR_OTICO + T13_ATRATOR_A5_A6 + T14_CONTROLE_AFIM -- R3.4 (19/10/2026): o replay dos runners CONGELADOS do F1.ATRATOR (copias byte a byte dos runners, dos pre-registros
# do ADENDO1 e do controle afim) contra os resultados arquivados, agora POR VERSAO: o pre-registro congelado pina o um.py v391 (caminho, sha256, bytes); a cada versao esse pino
# e repinado, NA COPIA do replay, para o um.py que o esboco MEDIU no Nos (marcadores {um_py_path} {um_py_sha256} {um_py_bytes}) e que o PINO DA CADEIA (PINO_UM_PY_vNNN.json,
# gerado por script a partir dos pinos da cadeia) confirma. Nada mais muda: o resto do pre-registro, os runners, os resultados arquivados e os outros 13 pinos ficam como estao.
# O adendo e declarado no resultado (antes/depois, copia e sha). O pino velho recusa: se o pino da cadeia nao e o um.py medido, o teste FALHA sem rodar runner nenhum.
# uso: t12_t14_atrator_r3_4.py <dir F1.ATRATOR do tunel> <dir destino (novo)> <saida.json> <PINO_UM_PY.json> <dir do Nos ({nos}; o um.py e <dir>/um.py)> <um_py_sha256> <um_py_bytes>
# (o um.py nao vai como argumento .py: o esboco so deixa passar .py pinado)
import datetime, hashlib, json, re, subprocess, sys
from pathlib import Path

SRC, DST, out, PINO = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), Path(sys.argv[4])
NOS_DIR, UM_SHA, UM_BYTES = Path(sys.argv[5]), sys.argv[6].lower(), int(sys.argv[7])
UM_PATH = NOS_DIR / "um.py"
RE_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def shab(b):
    return hashlib.sha256(b).hexdigest()


def falha(motivo, **extra):
    res = dict(teste="T12+T13+T14", veredito="FALHA", motivo=motivo, quando=datetime.datetime.now().isoformat(timespec="seconds"), **extra)
    with out.open("x", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)
    print("FALHA:", motivo)
    sys.exit(1)


def sem_duplicatas(pares):
    d = {}
    for k, v in pares:
        if k in d:
            raise ValueError("chave duplicada %r" % (k,))
        d[k] = v
    return d


# ---- 1. o pino da cadeia confirma o um.py que o esboco mediu (pino velho recusa)
try:
    pino = json.loads(PINO.read_bytes(), object_pairs_hook=sem_duplicatas)
except (OSError, ValueError) as exc:
    falha("PINO_ILEGIVEL: %s" % exc)
if (not isinstance(pino, dict) or pino.get("contrato") != "PINO_UM_PY_R3_4" or not isinstance(pino.get("versao"), str)
        or not isinstance(pino.get("um_py"), dict) or not RE_HEX64.match(str(pino["um_py"].get("sha256"))) or type(pino["um_py"].get("bytes")) is not int):
    falha("PINO_INVALIDO: PINO_UM_PY exige {contrato PINO_UM_PY_R3_4, versao, um_py {sha256, bytes}}")
if not RE_HEX64.match(UM_SHA) or UM_BYTES <= 0:
    falha("MARCADOR_INVALIDO: {um_py_sha256}/{um_py_bytes} do esboco")
if pino["um_py"]["sha256"] != UM_SHA or pino["um_py"]["bytes"] != UM_BYTES:
    falha("PINO_VELHO: o pino da cadeia (%s: um.py %s, %d B) nao e o um.py que o esboco mediu no Nos (%s, %d B); nenhum runner foi executado"
          % (pino["versao"], pino["um_py"]["sha256"][:16], pino["um_py"]["bytes"], UM_SHA[:16], UM_BYTES), pino_da_cadeia=pino["um_py"], medido=dict(sha256=UM_SHA, bytes=UM_BYTES))
if not UM_PATH.is_file():
    falha("UM_PY_AUSENTE: %s" % UM_PATH)
um_bytes = UM_PATH.read_bytes()
if shab(um_bytes) != UM_SHA or len(um_bytes) != UM_BYTES:
    falha("UM_PY_MUDOU_DEPOIS_DA_MEDIDA: %s tem %s (%d B) e o esboco mediu %s (%d B)" % (UM_PATH, shab(um_bytes)[:16], len(um_bytes), UM_SHA[:16], UM_BYTES))
um_texto = um_bytes.decode("utf-8-sig")
m_alpha = list(re.finditer(r"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n]+)\r?$", um_texto, re.MULTILINE))   # a mesma regex dos runners congelados
if len(m_alpha) != 1:
    falha("ALPHA_NAO_UNICA: %d atribuicoes de ALPHA_FINE_CODATA_2018 na coluna 0 do um.py" % len(m_alpha))
LINHA_ALPHA = um_texto[:m_alpha[0].start()].count("\n") + 1


# ---- 2. as copias: byte a byte, salvo o pino do um.py no PREREGISTRO_R1 (e o sha dele no RUN_MANIFEST_R3), repinados para o um.py medido
def cp(rel):
    s, d = SRC / rel, DST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    raw = s.read_bytes()
    with open(d, "xb") as f:
        f.write(raw)
    assert sha(d) == sha(s)
    return {"rel": rel, "sha256": sha(d), "bytes": len(raw)}


def deep_diff(a, b, path="$"):
    """os caminhos em que dois JSON diferem (lista)."""
    if isinstance(a, dict) and isinstance(b, dict):
        return [x for k in sorted(set(a) | set(b)) for x in (deep_diff(a.get(k), b.get(k), path + "." + k) if (k in a and k in b) else [path + "." + k + " (missing)"])]
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path + " (len)"]
        return [x for i, (u, v) in enumerate(zip(a, b)) for x in deep_diff(u, v, "%s[%d]" % (path, i))]
    return [] if a == b else [path]


def copiar_com_o_pino_repinado():
    s_pre = SRC / "PREREGISTRO_R1.json"
    raw = s_pre.read_bytes()
    pj = json.loads(raw, object_pairs_hook=sem_duplicatas)
    entradas = [x for x in pj["source_pins"] if Path(x["path"]).name == "um.py"]
    if len(entradas) != 1:
        falha("PREREGISTRO_SEM_PINO_UNICO_DO_UM_PY: %d entradas source_pins com nome um.py" % len(entradas))
    velho = entradas[0]
    novo_path = str(UM_PATH)
    # troca textual, so dos tres valores da entrada (cada um tem de aparecer exatamente uma vez no arquivo)
    trocas = [(velho["sha256"].encode("utf-8"), UM_SHA.encode("utf-8")), (b'"bytes": %d' % velho["bytes"], b'"bytes": %d' % UM_BYTES)]
    if velho["path"] != novo_path:
        trocas.append((json.dumps(velho["path"], ensure_ascii=False).encode("utf-8"), json.dumps(novo_path, ensure_ascii=False).encode("utf-8")))
    novo_raw = raw
    for a_, b_ in trocas:
        if novo_raw.count(a_) != 1:
            falha("PREREGISTRO_TROCA_NAO_UNICA: %r aparece %d vezes" % (a_[:70], novo_raw.count(a_)))
        novo_raw = novo_raw.replace(a_, b_)
    npj = json.loads(novo_raw, object_pairs_hook=sem_duplicatas)
    difs = deep_diff(pj, npj)
    permitidos = {"$.source_pins[%d].sha256" % pj["source_pins"].index(velho), "$.source_pins[%d].bytes" % pj["source_pins"].index(velho),
                  "$.source_pins[%d].path" % pj["source_pins"].index(velho)}
    if not difs or not set(difs) <= permitidos:
        falha("ADENDO_MUDA_ALEM_DO_PINO_DO_UM_PY: %s" % difs)
    d_pre = DST / "PREREGISTRO_R1.json"
    d_pre.parent.mkdir(parents=True, exist_ok=True)
    with open(d_pre, "xb") as f:
        f.write(novo_raw)
    # o RUN_MANIFEST_R3 pina o sha do pre-registro: repinado para a copia
    s_man = SRC / "numerical/RUN_MANIFEST_R3.json"
    mraw = s_man.read_bytes()
    a_, b_ = velho_prereg_sha(raw).encode("utf-8"), shab(novo_raw).encode("utf-8")
    if mraw.count(a_) != 1:
        falha("RUN_MANIFEST_TROCA_NAO_UNICA: o sha do pre-registro aparece %d vezes" % mraw.count(a_))
    d_man = DST / "numerical/RUN_MANIFEST_R3.json"
    d_man.parent.mkdir(parents=True, exist_ok=True)
    with open(d_man, "xb") as f:
        f.write(mraw.replace(a_, b_))
    return dict(arquivo="PREREGISTRO_R1.json", entrada_do_um_py=dict(antes=dict(path=velho["path"], sha256=velho["sha256"], bytes=velho["bytes"]),
                                                                    depois=dict(path=novo_path, sha256=UM_SHA, bytes=UM_BYTES)),
                caminhos_que_diferem=difs, original_sha256=shab(raw), copia_sha256=shab(novo_raw), copia_bytes=len(novo_raw),
                run_manifest_r3=dict(preregister_sha256_antes=shab(raw), preregister_sha256_depois=shab(novo_raw), copia_sha256=sha(d_man)),
                pino_da_cadeia=dict(versao=pino["versao"], contrato=pino["contrato"], sha256=sha(PINO)), preregister_sha256_da_copia=shab(novo_raw))


def velho_prereg_sha(raw):
    return shab(raw)


adendo = copiar_com_o_pino_repinado()
copies = [cp(r) for r in ("numerical/run_optical_r3.py", "ADENDO1/PREREGISTRO_ADENDO1_R1.json", "ADENDO1/numerical/run_adendo1_r1.py", "ADENDO1/numerical/RUN_MANIFEST_R1.json",
                          "review/verify_affine_control_r1.py")]
copies.append({"rel": "PREREGISTRO_R1.json", "sha256": adendo["copia_sha256"], "bytes": adendo["copia_bytes"], "repinada_para_o_um_py_medido": True})
copies.append({"rel": "numerical/RUN_MANIFEST_R3.json", "sha256": adendo["run_manifest_r3"]["copia_sha256"], "repinada_para_o_um_py_medido": True})

VOL = {"started_utc", "finished_utc", "elapsed_seconds", "environment", "began_utc", "ended_utc", "seconds", "created_utc", "python", "platform",
       "numpy", "path", "source_snapshot_before", "source_snapshot_after"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOL}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def diff(a, b, path="", acc=None):
    acc = acc if acc is not None else {"max_abs": 0.0, "mismatch": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                acc["mismatch"].append(path + "." + k + " (missing)")
                continue
            diff(a[k], b[k], path + "." + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mismatch"].append(path + " (len)")
            return acc
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, path + "[%d]" % i, acc)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        d = abs(float(a) - float(b))
        acc["max_abs"] = max(acc["max_abs"], d)
        if d != 0.0:
            acc["mismatch"].append(path + " (num %.3e)" % d)
    elif a != b:
        acc["mismatch"].append(path + " (value)")
    return acc


def esperado_t12(arq):
    """o resultado arquivado com SO os tres campos que dependem do um.py repinado trocados pelos valores independentes (a copia do pre-registro, o pino, a linha de alpha)."""
    e = json.loads(json.dumps(arq))
    for k in ("preregister_sha256", "um_sha256", "alpha_assignment_line"):
        if k not in e:
            falha("RESULTADO_ARQUIVADO_SEM_CAMPO: T12 sem %s" % k)
    e["preregister_sha256"], e["um_sha256"], e["alpha_assignment_line"] = adendo["preregister_sha256_da_copia"], UM_SHA, LINHA_ALPHA
    return e


def esperado_t13(arq):
    e = json.loads(json.dumps(arq))
    src = e.get("alpha_source")
    if not isinstance(src, dict) or "sha256" not in src or "line" not in src:
        falha("RESULTADO_ARQUIVADO_SEM_CAMPO: T13 sem alpha_source.sha256/line")
    src["sha256"], src["line"] = UM_SHA, LINHA_ALPHA
    n = 0
    for chave in ("sources_before", "sources_after"):
        lst = e.get(chave)
        if not isinstance(lst, list):
            falha("RESULTADO_ARQUIVADO_SEM_CAMPO: T13 sem %s" % chave)
        for x in lst:
            if Path(x["path"]).name == "um.py":
                x["sha256"] = UM_SHA
                n += 1
    if n != 2:
        falha("RESULTADO_ARQUIVADO_COM_PINO_DO_UM_PY_NAO_UNICO: %d entradas de um.py em sources_before/after (esperadas 2)" % n)
    return e


res = dict(teste="T12+T13+T14", versao_do_driver="R3.4", quando=datetime.datetime.now().isoformat(timespec="seconds"), copies=copies, adendo_de_pino=adendo,
           um_py_medido=dict(path=str(UM_PATH), sha256=UM_SHA, bytes=UM_BYTES, linha_de_alpha=LINHA_ALPHA), runs={})
ok_all = True
for name, rel, outrel, esp_fn in (("T12_optical_r3", "numerical/run_optical_r3.py", "numerical/RESULTADOS_NUMERICOS_R3.json", esperado_t12),
                                  ("T13_adendo1_r1", "ADENDO1/numerical/run_adendo1_r1.py", "ADENDO1/numerical/RESULTADOS_ADENDO1_R1.json", esperado_t13),
                                  ("T14_controle_afim", "review/verify_affine_control_r1.py", "review/ADENDO_CONTROLE_AFIM_R1.json", None)):
    script = DST / rel
    t0 = datetime.datetime.now(datetime.timezone.utc)
    r = subprocess.run([sys.executable, "-B", "-X", "utf8", str(script)], cwd=str(script.parent), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=1800)
    t1 = datetime.datetime.now(datetime.timezone.utc)
    log = DST / (rel + ".vinculo.log")
    with open(log, "x", encoding="utf-8") as f:
        f.write("START %s\nEND %s\nEXIT %d\nSTDOUT:\n%s\nSTDERR:\n%s\n" % (t0.isoformat(), t1.isoformat(), r.returncode, r.stdout, r.stderr))
    new, orig = DST / outrel, SRC / outrel
    e = dict(exit=r.returncode, log=str(log), log_sha256=sha(log), seconds=(t1 - t0).total_seconds())
    if r.returncode == 0 and new.exists():
        a = json.loads(new.read_bytes())
        b = json.loads(orig.read_bytes())
        if esp_fn is not None:
            b_esp = esp_fn(b)
            e["campos_trocados_no_arquivado"] = [k for k in deep_diff(b, b_esp)]
        else:
            b_esp = b
        d = diff(strip(a), strip(b_esp))
        e.update(result_new_sha256=sha(new), result_archived_sha256=sha(orig), max_abs_diff=d["max_abs"], n_mismatch=len(d["mismatch"]),
                 mismatch_sample=d["mismatch"][:25], all_expected_outcomes_met_new=a.get("all_expected_outcomes_met"),
                 beta_runtime_new=a.get("beta_runtime") or a.get("beta"), A6=(a.get("A6") or {}).get("status") if isinstance(a.get("A6"), dict) else None)
        e["passa"] = (len(d["mismatch"]) == 0)
    else:
        e["passa"] = False
    ok_all = ok_all and e["passa"]
    res["runs"][name] = e
res["veredito"] = "PASSA" if ok_all else "FALHA"
res["nota"] = ("A6 FALHA e o falsificador da minimalidade disparando como pre-registrado (identico ao arquivo), nao defeito. R3.4: so o pino do um.py foi repinado, na COPIA; "
               "os campos do resultado que dependem dele (sha do pre-registro, sha do um.py, linha de alpha) foram conferidos contra valores independentes, o resto contra o arquivado")
with out.open("x", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: (v["passa"], v.get("n_mismatch"), v["seconds"]) for k, v in res["runs"].items()}), res["veredito"])
sys.exit(0 if ok_all else 1)
