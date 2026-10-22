# SO LEITURA: a chave do pilar recalculada a partir do candidato (trabalhador + especificacao embutidos) e do beta_hex do resultado da v384
import ast, hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v385"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
def consts(path):
    out = {}
    for l in open(path, encoding="utf-8"):
        for nm in ("_QP_WORKER_SRC = ", "_QP_SPEC_JSON = ", "_QP_SPEC_SHA256 = "):
            if l.startswith(nm):
                out[nm.strip(" =")] = ast.literal_eval(l[len(nm):].strip())
    return out
c5 = consts(PK + r"\um_v385_candidato.py"); c4 = consts(NOS + r"\um.py")
print("v384 == v385 (trabalhador, spec, spec_sha):", all(c5[k] == c4[k] for k in c4), len(c4))
w = hashlib.sha256(c5["_QP_WORKER_SRC"].encode("utf-8")).hexdigest()
print("worker sha:", w[:16], "materializado no Nos:", hashlib.sha256(open(NOS + r"\quantum_pillar\pilar_quantico_worker.py", "rb").read()).hexdigest()[:16])
canon = json.dumps(json.loads(c5["_QP_SPEC_JSON"]), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
print("spec canon sha == _QP_SPEC_SHA256:", hashlib.sha256(canon.encode()).hexdigest() == c5["_QP_SPEC_SHA256"])
R = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca\result.json", encoding="utf-8"))
h = hashlib.sha256(); h.update(w.encode("ascii")); h.update(canon.encode("utf-8")); h.update(R["beta_hex"].encode("ascii"))
print("chave recalculada:", h.hexdigest()[:24], "== pasta do cache 75dc30bc9cc8d330e31f99ca:", h.hexdigest()[:24] == "75dc30bc9cc8d330e31f99ca")
core = json.load(open(NOS + r"\um_absoluto.json", encoding="utf-8"))["core"]
print("core beta hex:", float(core["beta"]).hex(), "== resultado:", float(core["beta"]).hex() == R["beta_hex"])
