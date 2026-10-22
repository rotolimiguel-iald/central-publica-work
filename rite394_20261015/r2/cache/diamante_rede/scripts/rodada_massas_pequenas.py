# -*- coding: utf-8 -*-
# Rodada complementar: massas menores (mℓ = 0.001, 0.003) para separar a primeira ordem das ordens superiores.
import os, sys, json, time
from multiprocessing import Pool
import diamante_rede as dr
if __name__ == '__main__':
    ells = [int(x) for x in sys.argv[1].split(',')]
    mells = sys.argv[2].split(',')
    tarefas = [(ell, me, s, dr.dps_para(ell)) for ell in ells for me in mells for s in (1, -1)]
    tarefas = [t for t in tarefas if not os.path.exists(os.path.join(dr.DADOS, 'H_l%d_m%s_s%+d_d%d.npz' % t))]
    print('tarefas', len(tarefas), flush=True)
    with Pool(processes=min(30, len(tarefas))) as pool:
        for r in pool.imap_unordered(dr.tarefa, tarefas):
            print(json.dumps(r), flush=True)
