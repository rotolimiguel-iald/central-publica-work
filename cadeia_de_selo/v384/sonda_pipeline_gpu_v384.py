# -*- coding: utf-8 -*-
"""SONDA 2 (so hardware) -- o custo de UMA instancia do pipeline completo do pilar quantico, com matrizes ALEATORIAS (nenhum operador da teoria,
nenhum desfecho olhado): superoperador GKLS com 5 saltos aleatorios + H aleatorio; espectro inteiro (eig); estado estacionario por LU com a linha do
traco; propagador expm(L dt); trajetoria de 64 passos a partir de 3 estados; 192 eigh d x d (entropias); matriz de Choi do propagador e seu menor
autovalor (eigvalsh). complex128, determinismo ligado, 4 fios de CPU (como no rito). Grava so tempos."""
import json, os, sys, time, platform
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_k] = "4"
import numpy as np
import torch
sys.stdout.reconfigure(encoding="utf-8")
torch.use_deterministic_algorithms(True)
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.set_num_threads(4)
dev = torch.device("cuda"); C = torch.complex128
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonda_pipeline_gpu_v384.json")
res = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "torch": torch.__version__, "gpu": torch.cuda.get_device_name(0), "dtype": "complex128",
       "fios_cpu": 4, "nota": "matrizes aleatorias; nenhum operador da teoria; servidor do modelo nativo LIGADO e ocioso", "por_d": {}}
g = torch.Generator(device="cpu").manual_seed(20261003)


def sync():
    torch.cuda.synchronize()


def crandn(*shape):
    return (torch.randn(*shape, dtype=torch.float64, generator=g) + 1j * torch.randn(*shape, dtype=torch.float64, generator=g)).to(C)


def superop(H, Ls):
    d = H.shape[-1]; I = torch.eye(d, dtype=C, device=H.device)
    S = -1j * (torch.kron(H, I) - torch.kron(I, H.T.contiguous()))
    for L in Ls:
        Lc = L.conj().resolve_conj().contiguous()
        LdL = (Lc.T.contiguous() @ L).contiguous()
        S = S + torch.kron(L, Lc) - 0.5 * torch.kron(LdL, I) - 0.5 * torch.kron(I, LdL.T.contiguous())
    return S


def choi(P, d):
    # row-stacking: P[(i*d+j),(k*d+l)] = <i|E(|k><l|)|j>; Choi[(i*d+k),(j*d+l)] = P[(i*d+j),(k*d+l)]
    return P.reshape(d, d, d, d).permute(0, 2, 1, 3).reshape(d * d, d * d).contiguous()


def instancia(d):
    t = {}
    A = crandn(d, d); H = ((A + A.conj().T) / 2).to(dev)
    Ls = [(crandn(d, d) / d).to(dev) for _ in range(5)]
    sync(); t0 = time.perf_counter(); S = superop(H, Ls); sync(); t["montar"] = time.perf_counter() - t0
    t0 = time.perf_counter(); ev = torch.linalg.eigvals(S); sync(); t["espectro_eigvals"] = time.perf_counter() - t0
    n = d * d
    t0 = time.perf_counter()
    M = S.clone(); M[0, :] = torch.eye(d, dtype=C, device=dev).reshape(-1)   # linha do traco
    b = torch.zeros(n, 1, dtype=C, device=dev); b[0, 0] = 1.0
    x = torch.linalg.solve(M, b); sync(); t["estacionario_lu"] = time.perf_counter() - t0
    t0 = time.perf_counter(); P = torch.linalg.matrix_exp(0.05 * S); sync(); t["propagador_expm"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    X = torch.zeros(n, 3, dtype=C, device=dev)
    for k in range(3):
        v = crandn(d, 1).to(dev); r = v @ v.conj().T; r = r / torch.trace(r); X[:, k] = r.reshape(-1)
    traj = []
    for s in range(64):
        X = P @ X; traj.append(X)
    R = torch.stack(traj).permute(0, 2, 1).reshape(64 * 3, d, d)
    R = (R + R.conj().transpose(-1, -2)) / 2
    w = torch.linalg.eigvalsh(R); sync(); t["trajetoria_64x3_e_entropias"] = time.perf_counter() - t0
    t0 = time.perf_counter(); Cm = choi(P, d); Cm = (Cm + Cm.conj().T) / 2; wc = torch.linalg.eigvalsh(Cm); del Cm; sync(); t["choi_eigvalsh"] = time.perf_counter() - t0
    t["total"] = sum(v for k, v in t.items())
    del S, M, P, X, R, ev, x, w, wc
    return t


for d, reps in ((8, 20), (16, 10), (32, 4), (64, 1)):
    ts = [instancia(d) for _ in range(reps)]
    med = {k: float(np.median([x[k] for x in ts])) for k in ts[0]}
    med["reps"] = reps; med["mem_pico_MiB"] = torch.cuda.max_memory_allocated() / 2 ** 20
    res["por_d"]["d%d" % d] = med
    print("d=%d" % d, json.dumps(med, ensure_ascii=False), flush=True)
    torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
open(OUT + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(OUT + ".tmp", OUT)
print("ok", OUT)
