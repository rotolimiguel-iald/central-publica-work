# -*- coding: utf-8 -*-
# O DIAMANTE PEQUENO NA REDE — o hamiltoniano modular de um intervalo no vácuo do férmion de Dirac massivo (1+1),
# na cadeia escalonada (staggered), em precisão alta. Gera os dados; a análise está em analisa_rede.py.
#
# Rede (espaçamento 1): h = -1/2 Σ (c_n† c_{n+1} + h.c.) + m Σ (-1)^n c_n† c_n.  No infinito, C = <c_i† c_j> é
#   C_ij = δ_ij/2 - [S1(i-j) + m (-1)^i G(i-j)]/2,  G(2j) = (2/π)(-1)^j Q_{j-1/2}(1+2m²)  (Heine),  S1(r) = -[G(r+1)+G(r-1)]/2 (r ímpar).
# Intervalo: sítios 0..N-1 (N = 2ℓ), com x_n = n - ℓ + 1/2.  Hamiltoniano modular (Peschel): H = log((1-C)/C), ρ ∝ exp(-Σ H_ij c_i† c_j).
# Isto é o mesmo objeto que H_V = -log(G_V^{-1} - 1) de Cadamuro–Fröb–Minz (G = <ψ ψ†> = 1 - C^T).
import mpmath as mp, numpy as np, os, sys, time, json
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__)); DADOS = os.path.join(AQUI, 'dados')

def G_even(j, m):
    q = mp.legenq(j - mp.mpf(1) / 2, 0, 1 + 2 * m * m, type=3)
    assert abs(mp.im(q)) <= mp.mpf(10) ** (-mp.mp.dps + 8) * (1 + abs(q)), 'Legendre Q com parte imaginária'
    return (2 / mp.pi) * (-1) ** j * mp.re(q)

def correl(N, m):
    Gs = {}
    def G(r):
        r = abs(r)
        if r % 2: return mp.mpf(0)
        if r not in Gs: Gs[r] = G_even(r // 2, m)
        return Gs[r]
    C = mp.matrix(N, N)
    for i in range(N):
        for j in range(i, N):
            r = i - j
            if r == 0: s1 = mp.mpf(0)
            elif r % 2:
                s1 = (-(2 / mp.pi) * mp.sin(r * mp.pi / 2) / r) if m == 0 else (-(G(r + 1) + G(r - 1)) / 2)
            else: s1 = mp.mpf(0)
            mass = (m * (-1) ** i * G(r)) if (m != 0 and r % 2 == 0) else mp.mpf(0)
            v = (mp.mpf(1) / 2 if r == 0 else mp.mpf(0)) - (s1 + mass) / 2
            C[i, j] = v; C[j, i] = v
    return C

def tarefa(args):
    ell, mell, sinal, dps = args
    mp.mp.dps = dps; t0 = time.time(); N = 2 * ell
    m = mp.mpf(0) if mell == '0' else sinal * mp.mpf(mell) / ell
    C = correl(N, m)
    E, Q = mp.eigsy(C)
    nu = [E[k] for k in range(N)]
    numin = min(nu); numax = max(nu)
    assert numin > mp.mpf(10) ** (-dps + 25) and 1 - numax > mp.mpf(10) ** (-dps + 25), 'precisão insuficiente: autovalor perto de 0/1'
    eps = np.array([float(mp.log((1 - v) / v)) for v in nu])
    Qf = np.array([[float(Q[i, k]) for k in range(N)] for i in range(N)])
    Cf = np.array([[float(C[i, j]) for j in range(N)] for i in range(N)])
    H = (Qf * eps) @ Qf.T
    # reconstrução em float (diagnóstico) e ortogonalidade
    rec = float(np.abs((Qf * np.array([float(v) for v in nu])) @ Qf.T - Cf).max())
    nome = 'H_l%d_m%s_s%+d_d%d.npz' % (ell, mell, sinal, dps)
    np.savez_compressed(os.path.join(DADOS, nome), H=H, C=Cf, eps=eps, ell=ell, mell=mell, sinal=sinal, dps=dps)
    return {'arquivo': nome, 'ell': ell, 'mell': mell, 'sinal': sinal, 'dps': dps, 'nu_min': mp.nstr(numin, 5),
            'eps_max': float(max(abs(eps))), 'reconstrucao': rec, 'segundos': round(time.time() - t0, 1)}

def dps_para(ell):
    return int(0.85 * 2 * ell) + 45

if __name__ == '__main__':
    os.makedirs(DADOS, exist_ok=True)
    ells = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else '16,24,32,48,64'.split(','))]
    mells = ['0.01', '0.03', '0.1']
    tarefas = []
    for ell in ells:
        d = dps_para(ell)
        tarefas.append((ell, '0', 1, d))
        for me in mells:
            for s in (1, -1):
                tarefas.append((ell, me, s, d))
    # controle de precisão: o mesmo caso com +40 dígitos
    for ell in [e for e in ells if e in (32, 64)]:
        for s in (1, -1):
            tarefas.append((ell, '0.03', s, dps_para(ell) + 40))
    tarefas = [t for t in tarefas if not os.path.exists(os.path.join(DADOS, 'H_l%d_m%s_s%+d_d%d.npz' % t))]
    tarefas.sort(key=lambda t: -t[0])
    print('tarefas:', len(tarefas), flush=True)
    t0 = time.time(); log = []
    with Pool(processes=min(44, max(1, len(tarefas)))) as pool:
        for r in pool.imap_unordered(tarefa, tarefas):
            log.append(r); print(json.dumps(r), flush=True)
    json.dump(log, open(os.path.join(DADOS, 'log_%d.json' % int(time.time())), 'w'), indent=1)
    print('total %.0fs' % (time.time() - t0))
