# -*- coding: utf-8 -*-
"""SONDA DE TEMPO da RTX 5090 para dimensionar o pilar quantico da v384 -- mede SO o hardware: matrizes ALEATORIAS (nenhum operador da teoria, nenhum desfecho),
complex128, com as chaves de determinismo ligadas. Para cada dimensao d do sistema (o superoperador tem d^2 x d^2): montar o superoperador GKLS de 5 saltos
aleatorios, exponencial (expm), autovalores (eig, nao Hermitiano), nucleo (SVD) e lotes de expm; a CPU (numpy) ao lado para a referencia. Grava so o JSON
de tempos no scratchpad. Memoria pequena (o servidor do modelo nativo segue ligado)."""
import json, os, sys, time, platform
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_k] = "4"   # a CPU de referencia com 4 fios, como ficara durante o rito (o lake build usa o resto)
import numpy as np
import torch
sys.stdout.reconfigure(encoding="utf-8")
torch.use_deterministic_algorithms(True)
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.set_num_threads(2)
dev = torch.device("cuda")
C = torch.complex128
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonda_tempo_gpu_v384.json")
res = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "torch": torch.__version__, "cuda": torch.version.cuda, "gpu": torch.cuda.get_device_name(0),
       "numpy": np.__version__, "python": platform.python_version(), "dtype": "complex128", "determinismo": {"use_deterministic_algorithms": True,
       "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"), "tf32": False}, "medidas": {}}


def sync():
    torch.cuda.synchronize()


def tempo(f, rep=3):
    ts = []
    for _ in range(rep):
        sync(); t0 = time.perf_counter(); f(); sync(); ts.append(time.perf_counter() - t0)
    return float(np.median(ts))


def superop(H, Ls):
    d = H.shape[-1]; I = torch.eye(d, dtype=C, device=H.device)
    S = -1j * (torch.kron(H, I) - torch.kron(I, H.T.contiguous()))   # convencao row-stacking so para a sonda (o custo nao depende dela)
    for L in Ls:
        Lc = L.conj().resolve_conj().contiguous()
        LdL = (Lc.T.contiguous() @ L).contiguous()
        S = S + torch.kron(L, Lc) - 0.5 * torch.kron(LdL, I) - 0.5 * torch.kron(I, LdL.T.contiguous())
    return S


g = torch.Generator(device="cpu").manual_seed(20261003)


def aleatorio(d):
    A = torch.randn(d, d, dtype=torch.float64, generator=g) + 1j * torch.randn(d, d, dtype=torch.float64, generator=g)
    H = ((A + A.conj().T) / 2).to(C)
    Ls = [((torch.randn(d, d, dtype=torch.float64, generator=g) + 1j * torch.randn(d, d, dtype=torch.float64, generator=g)) / d).to(C) for _ in range(5)]
    return H, Ls


# 1. vazao FP64 complexa da placa (GEMM)
n = 4096; Ag = torch.randn(n, n, dtype=C, device=dev); Bg = torch.randn(n, n, dtype=C, device=dev)
tg = tempo(lambda: Ag @ Bg)
res["medidas"]["gemm_complex128_4096"] = {"s": tg, "tflops_reais": 8 * n ** 3 / tg / 1e12}
del Ag, Bg; torch.cuda.empty_cache()
# 2. por dimensao
for d in (8, 16, 32, 64):
    H, Ls = aleatorio(d)
    Hg, Lg = H.to(dev), [L.to(dev) for L in Ls]
    m = {}
    m["montar_s"] = tempo(lambda: superop(Hg, Lg))
    S = superop(Hg, Lg)
    m["expm_s"] = tempo(lambda: torch.linalg.matrix_exp(0.37 * S))
    m["eig_s"] = tempo(lambda: torch.linalg.eig(S), rep=1 if d >= 64 else 3)
    m["svd_nucleo_s"] = tempo(lambda: torch.linalg.svd(S), rep=1 if d >= 64 else 3)
    Sc = S.cpu().numpy()
    t0 = time.perf_counter(); np.linalg.eig(Sc); m["eig_cpu_numpy_s"] = time.perf_counter() - t0
    import scipy.linalg as sl
    t0 = time.perf_counter(); sl.expm(0.37 * Sc); m["expm_cpu_scipy_s"] = time.perf_counter() - t0
    if d <= 32:
        B = 256 if d <= 16 else 8
        Sb = S.unsqueeze(0).repeat(B, 1, 1) * torch.linspace(0.1, 1.0, B, dtype=torch.float64, device=dev).to(C).view(B, 1, 1)
        m["expm_lote"] = {"B": B, "s": tempo(lambda: torch.linalg.matrix_exp(Sb)), "s_por_matriz": None}
        m["expm_lote"]["s_por_matriz"] = m["expm_lote"]["s"] / B
        del Sb
    m["mem_pico_MiB"] = torch.cuda.max_memory_allocated() / 2 ** 20
    res["medidas"]["d%d" % d] = m
    print("d=%d" % d, json.dumps(m, ensure_ascii=False), flush=True)
    del S, Hg, Lg; torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
open(OUT + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(OUT + ".tmp", OUT)
print("gemm complex128 4096: %.3f s, %.2f TFLOP/s reais" % (tg, res["medidas"]["gemm_complex128_4096"]["tflops_reais"]))
print("ok", OUT)
