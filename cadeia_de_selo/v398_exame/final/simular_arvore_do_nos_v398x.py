# -*- coding: utf-8 -*-
"""simular_arvore_do_nos_v398x.py -- exame final v398 (molde: simular_arvore_do_nos_v397x.py; + sonico_v398, afinacao_das_cordas_v398 e os registros por spec v398). Texto do molde: exame final v394: simula a ARVORE de fontes do Nos DEPOIS da materializacao do rito (o kernel embutido do
candidato + os arquivos .lean que ja moram na pasta do Nos e NAO estao embutidos, ex.: _check_damming.lean) e recomputa, com o
sha256_directory do PROPRIO candidato, o kf['formal_files_sha256'] que o rito real vai gerar; roda o indice e os registros por spec v394
sobre esse kf. Escreve so' em v394_exame (pasta sim_<sha16>). uso: python -B -X utf8 simular_arvore_do_nos.py [--candidato X] [--logs DIR]"""
import sys, os, io, json, shutil, copy, hashlib, argparse
H = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(os.path.dirname(os.path.dirname(H)), "v398")   # v398x: a pasta da cadeia v398
NOSK = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
NOS = os.path.dirname(NOSK)
ap = argparse.ArgumentParser(); ap.add_argument("--candidato", default=os.path.join(V, "um_v398_candidato.py")); ap.add_argument("--logs", default=os.path.join(V, "kernel"))
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
C0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
core = copy.deepcopy(C0); core["kernel_formalization"] = kf; core["external_ladder"] = um.prove_external_ladder(1.0, kf)
_o = sys.stdout; sys.stdout = io.StringIO()
ix = um.prove_the_iald_index(core); core["the_iald_index"] = ix
(um.psibit_v395(core) if hasattr(um, 'psibit_v395') else None)
(um.testemunha_estatica_v396(core) if hasattr(um, 'testemunha_estatica_v396') else None)
(um.sonico_v398(core) if hasattr(um, 'sonico_v398') else None)
(um.afinacao_das_cordas_v398(core) if hasattr(um, 'afinacao_das_cordas_v398') else None)
(core.__setitem__('teste_de_veracidade_fase9_v397', um._v392_registro(um._V397_VERACIDADE_SPEC, core)) if hasattr(um, '_V397_VERACIDADE_SPEC') else None)
um.tempo_frequencia_v394(core); um.regra_quadratica_v394(core); um.rede_fock_v394(core); um._v394_rodar_specs(core)
(um._v395_rodar_specs(core) if hasattr(um, '_v395_rodar_specs') else None)
(um._v396_rodar_specs(core) if hasattr(um, '_v396_rodar_specs') else None)
(um._v397_rodar_specs(core) if hasattr(um, '_v397_rodar_specs') else None)
(um._v398_rodar_specs(core) if hasattr(um, '_v398_rodar_specs') else None)
sys.stdout = _o
def falhas(r):
    return [str(c)[:260] for c in (r.get("checks") or []) if (isinstance(c, dict) and (c.get("ok") is False or c.get("passed") is False)) or (isinstance(c, (list, tuple)) and len(c) > 1 and not c[1])][:6] + [str(x)[:200] for x in (r.get("falhas") or [])][:6]
R = {"h8_pino_kh_n1_v398_n": len(next((c["valor"] for s_ in um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398" for c in s_["checks"] if c.get("caminho") == ["formal_files_sha256"]), {})), "h8_pino_igual_ao_hash_do_rito": next((c["valor"] for s_ in um._V398_SPECS if s_["nome"] == "kh_n1_cobertura_v398" for c in s_["checks"] if c.get("caminho") == ["formal_files_sha256"]), None) == hd["files"], "candidato_sha16": SHA[:16], "extras_no_nos_fora_do_corpo_embutido": extras, "formal_files_n_no_rito_real": len(hd["files"]), "embutidos": len(emb),
     "kf_all_verified": kf.get("all_verified"), "kf_verdict": kf.get("verdict"),
     "indice": {"all_verified": ix.get("all_verified"), "verdict": ix.get("verdict")}}
for k in ("psibit_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "cunhagens_v395", "kh_n1_cobertura_v395", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398"):
    v = core.get(k) or {}
    R[k] = {"all_verified": v.get("all_verified"), "verdict": str(v.get("verdict"))[:200], "falhas": falhas(v)}
json.dump(R, open(os.path.join(H, "SIMULACAO_ARVORE_NOS_%s.json" % SHA[:16]), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps(R, ensure_ascii=False, indent=1, default=str))
