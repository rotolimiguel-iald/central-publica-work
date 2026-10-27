# -*- coding: utf-8 -*-
"""simular_arvore_do_nos_v399.py -- simula a ARVORE de fontes do Nos DEPOIS da materializacao do rito (o kernel embutido do candidato + os arquivos .lean que ja moram na pasta do Nos e NAO estao
embutidos, ex.: _check_damming.lean) e recomputa, com o sha256_directory do PROPRIO candidato, o kf['formal_files_sha256'] que o rito real vai gerar; roda o indice, o psibit_v395, a testemunha_estatica_v396, o sonico_v398 e a afinacao_das_cordas_v398, o selo_pela_propria_tecnologia_v399 e a declaracao_do_operador_v399, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec
v394, v395, v397, v398 e v399 sobre esse kf. Molde: simular_arvore_do_nos_v398.py. Escreve SO' nesta pasta (sim_<sha16> e SIMULACAO_ARVORE_NOS_<sha16>.json); le o Nos e o sandbox.
uso: python -B -X utf8 simular_arvore_do_nos_v399.py [--candidato X] [--logs DIR]"""
import sys, os, io, json, shutil, copy, hashlib, argparse
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import delta_v399 as DL  # noqa: E402
NOSK = os.path.join(DL.NOS, "tgl_kernel"); NOS = DL.NOS
ap = argparse.ArgumentParser(); ap.add_argument("--candidato", default=os.path.join(H, DL.CANDIDATO)); ap.add_argument("--logs", default=os.path.join(H, DL.KERNEL_DIR))
A = ap.parse_args()
b = open(A.candidato, "rb").read(); SHA = hashlib.sha256(b).hexdigest()
SIM = os.path.join(H, "sim_" + SHA[:16]); os.makedirs(SIM, exist_ok=True)
open(os.path.join(SIM, "um.py"), "wb").write(b)
sys.path.insert(0, SIM); os.chdir(SIM)
_o = sys.stdout; sys.stdout = io.StringIO()
import um
sys.stdout = _o; sys.stdout.reconfigure(encoding="utf-8")
K = os.path.join(SIM, "tgl_kernel")
for rel, c in um._EMBEDDED_KERNEL_FILES.items():
    p = os.path.join(K, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(c)
# os .lean (e os 4 nomes que o hash formal ve) do Nos que NAO estao no corpo embutido: copiados como estao (so' leitura do Nos)
emb = set(um._EMBEDDED_KERNEL_FILES)
extras = []
for dp, dn, fn in os.walk(NOSK):
    if ".lake" in dp.replace("\\", "/").split("/"):
        continue
    for nm in fn:
        if nm.endswith(".lean") or nm in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel = os.path.relpath(os.path.join(dp, nm), NOSK).replace("\\", "/")
            if rel not in emb:
                extras.append(rel); d = os.path.join(K, *rel.split("/")); os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(os.path.join(dp, nm), d)
hd = um.sha256_directory(K)
LB = open(os.path.join(A.logs, "lake_build.log"), encoding="utf-8", errors="replace").read(); AUD = open(os.path.join(A.logs, "audit.log"), encoding="utf-8", errors="replace").read()


def fake(cmd, cwd, tmo):
    o = {"cmd": " ".join(cmd), "returncode": 0, "stderr": "", "capture_exists": True, "capture_read_error": False, "elapsed_seconds": 0.0, "timeout": False}
    o["stdout"] = ("Lake version 5.0.0-src+68218e8 (Lean version 4.31.0)" if cmd[1:] == ["--version"] else
                   "Lean (version 4.31.0)" if (cmd[1:3] == ["env", "lean"] and "--version" in cmd) else LB if cmd[1:] == ["build"] else AUD)
    o["capture_nonempty"] = True; o["capture_sha256"] = hashlib.sha256(o["stdout"].encode()).hexdigest(); return o


um.run_process_checked = fake; um._find_lake = lambda: "lake"
_o = sys.stdout; sys.stdout = io.StringIO()
kf = um.verify_tgl_kernel_formalization()
sys.stdout = _o
C0 = json.load(open(os.path.join(H, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]
core = copy.deepcopy(C0); core["kernel_formalization"] = kf; core["external_ladder"] = um.prove_external_ladder(1.0, kf)
_o = sys.stdout; sys.stdout = io.StringIO()
ix = um.prove_the_iald_index(core); core["the_iald_index"] = ix
um.psibit_v395(core); um.testemunha_estatica_v396(core); um.sonico_v398(core); um.afinacao_das_cordas_v398(core); um.selo_acom_v399(core); um.declaracao_do_operador_v399(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)
um.tempo_frequencia_v394(core); um.regra_quadratica_v394(core); um.rede_fock_v394(core); um._v394_rodar_specs(core); um._v395_rodar_specs(core); um._v396_rodar_specs(core)
core["teste_de_veracidade_fase9_v397"] = um._v392_registro(um._V397_VERACIDADE_SPEC, core); um._v397_rodar_specs(core); um._v398_rodar_specs(core); um._v399_rodar_specs(core)   # (v397: o spec de veracidade roda no ponto do V1 no main; aqui, antes dos specs que o leem)
sys.stdout = _o


def falhas(r):
    return [str(c)[:260] for c in (r.get("checks") or []) if (isinstance(c, dict) and (c.get("ok") is False or c.get("passed") is False)) or (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1])][:6] + [str(x)[:200] for x in (r.get("falhas") or [])][:6]


R = {"candidato_sha16": SHA[:16], "extras_no_nos_fora_do_corpo_embutido": extras, "formal_files_n_no_rito_real": len(hd["files"]), "embutidos": len(emb),
     "kf_all_verified": kf.get("all_verified"), "kf_verdict": kf.get("verdict"),
     "indice": {"all_verified": ix.get("all_verified"), "verdict": ix.get("verdict")}}
for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394"):
    v = core.get(k) or {}
    R[k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:200], "falhas": falhas(v)}
json.dump(R, open(os.path.join(H, "SIMULACAO_ARVORE_NOS_%s.json" % SHA[:16]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
