# -*- coding: utf-8 -*-
"""
d1_v3_pipeline.py — o pipeline da V3 do D1 (protocolo D1_CAMB_V3 da v363, hash d5c35ea6d20b76eb), construído CEGO.

MODOS
  autoverificacao   : o worker V3 em β = 0 contra o CAMB, fecho E(0) = 1, segunda equação de Friedmann, limites de w constante.
  injecao           : dados SINTÉTICOS gerados pelo próprio modelo em β injetado (sem ruído e com K realizações de ruído da covariância),
                      ajustados pelo pipeline; mede viés, pulls e cobertura. Os VALORES CENTRAIS dos dados reais NÃO são usados.
  real              : TRANCADO. Recusa (código 3) sem o arquivo CONFIRMACAO_OPERADOR_ROTA_V3.json com a linha do operador e o hash do
                      protocolo. A rota do fundo veio por repasse; a confirmação de uma linha é pré-condição escrita no protocolo.

Dados do primário (idênticos ao script de maio, tgl_mcmc_camb_v2.py): Planck 2018 comprimido (R, l_A, ω_b; Zhai+ 2019) + DESI DR1 BAO
(Adame+ 2024). SH0ES FORA do ajuste de fundo no primário; variante com SH0ES ao lado. C = 0 primário; C livre = sensibilidade.
Matriz de vereditos: a da V2, inalterada (Δχ² 4/25; bondade de ajuste χ²_ΛCDM ≤ 3 × n_dados; autoverificação 5e-3 RELIDA; régua do β).
β nunca literal: ALPHA_FINE_CODATA_2018 × √e em tempo de execução. Vereditos proibidos: CONFIRMED, PROVED.
"""
import os, sys, json, time, hashlib
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import tgl_camb_worker_v3 as W

PROTOCOLO_V3 = 'd5c35ea6d20b76eb'
ALPHA_FINE_CODATA_2018 = 0.0072973525693


def beta_tgl():
    return ALPHA_FINE_CODATA_2018 * float(np.sqrt(np.e))


# ---- dados do primário (copiados do script de maio; os valores centrais só são lidos no modo real) ----
PLANCK_COV = np.array([[2.1167e-05, 3.4659e-05, -4.5466e-08], [3.4659e-05, 8.0901e-03, -1.6087e-06], [-4.5466e-08, -1.6087e-06, 2.2497e-08]])
DESI_ROWS = [(0.295, 2, 0.15), (0.510, 0, 0.25), (0.510, 1, 0.61), (0.706, 0, 0.32), (0.706, 1, 0.60), (0.930, 0, 0.28), (0.930, 1, 0.35),
             (1.317, 0, 0.69), (1.317, 1, 0.42), (1.491, 2, 0.67), (2.330, 0, 0.94), (2.330, 1, 0.17)]
DESI_Z = sorted(set(r[0] for r in DESI_ROWS))
SH0ES_SIGMA = 1.04


def _dados_reais():
    """Só o modo real chama isto (depois da tranca)."""
    return dict(planck_mean=np.array([1.7502, 301.471, 0.02236]),
                desi_vals=np.array([7.93, 13.62, 20.98, 16.85, 20.08, 21.71, 17.88, 27.79, 13.82, 26.07, 39.71, 8.52]),
                sh0es_mean=73.04)


CRITERIOS = dict(delta_chi2_5sigma=25.0, delta_chi2_2sigma=4.0, gof_fator=3.0, selfcheck_tol=5e-3,
                 regra_mcmc='FALSIFIED se alpha sqrt(e) fora de 5 sigma; INCAPAZ se sigma(beta) > beta; NOT_FALSIFIED_POWERED se sigma <= beta/2 '
                            'e alpha sqrt(e) dentro de 3 sigma; TENSION se fora de 3 sigma; INCONCLUSIVE nos demais')
LIMITES = dict(H0=(50.0, 90.0), ombh2=(0.015, 0.030), omch2=(0.08, 0.18), beta=(-0.05, 0.05), c=(-0.05, 0.05))
ESCALA = np.array([1.0, 0.0005, 0.005, 0.005, 0.005])
FIDUCIAL = np.array([67.5, 0.02237, 0.1200, 0.0, 0.0])


def predicao(theta):
    H0, ombh2, omch2, beta, c = theta
    d = W.derivados(dict(beta=beta, H0=H0, ombh2=ombh2, omch2=omch2, c=c, desi_z=DESI_Z))
    rd = d['r_drag_TGL']; idx = {z: i for i, z in enumerate(d['desi_z'])}
    desi = []
    for z, kind, _ in DESI_ROWS:
        DM = d['DM_at_DESI'][idx[z]]; DH = W.C_KMS / d['H_at_DESI'][idx[z]]
        desi.append(DM / rd if kind == 0 else (DH / rd if kind == 1 else (z * DM * DM * DH) ** (1.0 / 3.0) / rd))
    return np.array([d['R'], d['lA'], ombh2]), np.array(desi), H0, d


def dentro(theta, livre_c):
    nomes = ['H0', 'ombh2', 'omch2', 'beta'] + (['c'] if livre_c else [])
    return all(LIMITES[n][0] < theta[i] < LIMITES[n][1] for i, n in enumerate(nomes))


_LCHOL = np.linalg.cholesky(PLANCK_COV)


def residuos(theta, dados, usar_sh0es):
    """Resíduos branqueados: χ² = |r|² (Planck pela Cholesky da covariância; DESI e SH0ES por σ)."""
    pl, de, H0, d = predicao(theta)
    from scipy.linalg import solve_triangular
    r = [solve_triangular(_LCHOL, pl - dados['planck_mean'], lower=True), (de - dados['desi_vals']) / np.array([r_[2] for r_ in DESI_ROWS])]
    if usar_sh0es:
        r.append(np.array([(H0 - dados['sh0es_mean']) / SH0ES_SIGMA]))
    return np.concatenate(r), d


def chi2(theta, dados, usar_sh0es):
    livre_c = abs(theta[4]) > 0 or dados.get('livre_c', False)
    if not dentro(theta, livre_c):
        return np.inf, None
    try:
        r, d = residuos(theta, dados, usar_sh0es)
    except Exception:
        return np.inf, None
    return float(r @ r), d


def ajuste(dados, usar_sh0es, beta_fixo=None, livre_c=False, x0=None, reinicios=1):
    """Mínimos quadrados (região de confiança com limites) em coordenadas escaladas y: θ = base + s·y."""
    from scipy.optimize import least_squares
    base = np.array(FIDUCIAL, float)
    ini = np.array(FIDUCIAL if x0 is None else x0, float)
    livres = [0, 1, 2] + ([] if beta_fixo is not None else [3]) + ([4] if livre_c else [])
    nomes = ['H0', 'ombh2', 'omch2', 'beta', 'c']

    def monta(y):
        th = base.copy()
        if beta_fixo is not None: th[3] = beta_fixo
        th[4] = 0.0
        th[livres] = base[livres] + ESCALA[livres] * y
        return th

    lo = np.array([(LIMITES[nomes[k]][0] - base[k]) / ESCALA[k] for k in livres]) * 0.999
    hi = np.array([(LIMITES[nomes[k]][1] - base[k]) / ESCALA[k] for k in livres]) * 0.999
    y = (ini[livres] - base[livres]) / ESCALA[livres]
    fun = lambda yy: residuos(monta(yy), dados, usar_sh0es)[0]
    res = None; nfev = 0
    for _ in range(reinicios + 1):
        res = least_squares(fun, y, bounds=(lo, hi), method='trf', jac='3-point', diff_step=1e-3, x_scale=1.0,
                            xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=400)
        y = res.x; nfev += int(res.nfev)
    th = monta(res.x); x2, d = chi2(th, dados, usar_sh0es)
    J = res.jac
    try:
        cov = np.linalg.inv(J.T @ J)
        sig_b = float(ESCALA[3] * np.sqrt(cov[livres.index(3), livres.index(3)])) if 3 in livres else None
    except Exception:
        sig_b = None
    return dict(theta=th.tolist(), chi2=x2, sucesso=bool(np.isfinite(x2) and res.status > 0), nfev=nfev, livres=livres, sigma_beta_JtJ=sig_b,
                selfcheck=(d or {}).get('dm_selfcheck_ratio'), residuo_segunda=(d or {}).get('second_friedmann_residual'),
                fecho_E0=(d or {}).get('E_at_z0'))


def sigma_fisher(th, dados, usar_sh0es, livres, passo=0.3):
    """σ(β) pela matriz JᵀJ recalculada no ponto (Jacobiana central em coordenadas escaladas)."""
    th = np.array(th, float); n = len(livres); h = 1e-3
    f0 = residuos(th, dados, usar_sh0es)[0]; J = np.zeros((f0.size, n))
    for i, k in enumerate(livres):
        tp = th.copy(); tm = th.copy(); tp[k] += ESCALA[k] * h; tm[k] -= ESCALA[k] * h
        J[:, i] = (residuos(tp, dados, usar_sh0es)[0] - residuos(tm, dados, usar_sh0es)[0]) / (2 * h)
    cov = np.linalg.inv(J.T @ J)
    return float(ESCALA[3] * np.sqrt(cov[livres.index(3), livres.index(3)]))


def dados_sinteticos(theta_inj, semente=None, livre_c=False):
    pl, de, H0, d = predicao(np.array(theta_inj, float))
    out = dict(planck_mean=pl.copy(), desi_vals=de.copy(), sh0es_mean=H0, livre_c=livre_c)
    if semente is not None:
        rng = np.random.default_rng(semente)
        out['planck_mean'] = pl + rng.multivariate_normal(np.zeros(3), PLANCK_COV)
        out['desi_vals'] = de + rng.normal(0.0, 1.0, len(de)) * np.array([r[2] for r in DESI_ROWS])
        out['sh0es_mean'] = H0 + rng.normal(0.0, SH0ES_SIGMA)
    return out, d


def _uma_realizacao(args):
    theta_inj, semente, usar_sh0es, livre_c = args
    dados, _ = dados_sinteticos(theta_inj, semente, livre_c)
    x0 = np.array(FIDUCIAL, float); x0[0] += 0.8; x0[2] += 0.002   # partida longe da verdade
    bf = ajuste(dados, usar_sh0es, livre_c=livre_c, x0=x0)
    sig = sigma_fisher(bf['theta'], dados, usar_sh0es, bf['livres']) if bf['sucesso'] else None
    return dict(semente=semente, beta_hat=bf['theta'][3], sigma=sig, chi2=bf['chi2'], selfcheck=bf['selfcheck'],
                residuo_segunda=bf['residuo_segunda'], fecho_E0=bf['fecho_E0'], nfev=bf['nfev'], c_hat=bf['theta'][4])


def _logpost_4(t4, dados, usar_sh0es):
    x2, _ = chi2(np.array([t4[0], t4[1], t4[2], t4[3], 0.0]), dados, usar_sh0es)
    return -0.5 * x2 if np.isfinite(x2) else -np.inf


def _logpost_5(t5, dados, usar_sh0es):
    x2, _ = chi2(np.array(t5, float), dados, usar_sh0es)
    return -0.5 * x2 if np.isfinite(x2) else -np.inf


def fase3_mcmc(dados, usar_sh0es, livre_c, nproc, n_walkers=24, n_steps=2000, burn=400, semente=42):
    """Fase 3 (a única cega no protocolo): emcee com β livre, como na V2 (24 caminhantes × 2000 passos, queima 400)."""
    import emcee
    from multiprocessing import Pool
    ndim = 5 if livre_c else 4
    rng = np.random.default_rng(semente)
    p0 = FIDUCIAL[:ndim].copy()
    larg = np.array([1.0, 0.0005, 0.005, 0.005, 0.005])[:ndim]
    pos = p0 + rng.normal(0, 1, size=(n_walkers, ndim)) * larg
    for i in range(n_walkers):
        while not dentro(np.concatenate([pos[i], np.zeros(5 - ndim)]), livre_c):
            pos[i] = p0 + rng.normal(0, 1, size=ndim) * larg * 0.5
    fn = _logpost_5 if livre_c else _logpost_4
    t0 = time.time()
    with Pool(nproc) as pool:
        sampler = emcee.EnsembleSampler(n_walkers, ndim, fn, args=(dados, usar_sh0es), pool=pool)
        sampler.run_mcmc(pos, n_steps, progress=False)
    ch = sampler.get_chain(discard=burn, flat=True)
    nomes = ['H0', 'ombh2', 'omch2', 'beta', 'c'][:ndim]
    resumo = {}
    for i, nm in enumerate(nomes):
        med = float(np.median(ch[:, i])); lo = float(np.percentile(ch[:, i], 16)); hi = float(np.percentile(ch[:, i], 84))
        resumo[nm] = dict(median=med, lo16=lo, hi84=hi, sigma_lower=med - lo, sigma_upper=hi - med)
    try:
        tau = [float(v) for v in sampler.get_autocorr_time(quiet=True)]
    except Exception:
        tau = None
    return dict(summary=resumo, acceptance_fraction_mean=float(np.mean(sampler.acceptance_fraction)), chain_size=int(len(ch)),
                n_walkers=n_walkers, n_steps=n_steps, burn=burn, autocorr_time=tau, time_seconds=round(time.time() - t0, 1))


def matriz_v2(delta_chi2, chi2_lcdm, n_dados, selfchecks, beta_med, beta_sig):
    """A matriz de vereditos da V2, inalterada, com a bondade de ajuste 3 × n_dados e a autoverificação RELIDA em reasons."""
    bt = beta_tgl(); reasons = []
    if not (isinstance(chi2_lcdm, float) and chi2_lcdm <= CRITERIOS['gof_fator'] * n_dados):
        reasons.append('chi^2 LCDM %s > %.0f (bondade de ajuste)' % (chi2_lcdm, CRITERIOS['gof_fator'] * n_dados))
    ruins = [x for x in selfchecks if not (isinstance(x, float) and abs(x - 1.0) < CRITERIOS['selfcheck_tol'])]
    if ruins:
        reasons.append('autoverificacao DM(beta=0)/DM_CAMB fora de 5e-3: %s' % ruins)
    if reasons or not isinstance(delta_chi2, float):
        bf = 'INCONCLUSIVE_SYSTEMATICS'
    elif delta_chi2 >= CRITERIOS['delta_chi2_5sigma']: bf = 'D1_LCDM_PREFERRED_5SIGMA'
    elif delta_chi2 <= -CRITERIOS['delta_chi2_5sigma']: bf = 'D1_TGL_BACKGROUND_PREFERRED_5SIGMA'
    elif abs(delta_chi2) >= CRITERIOS['delta_chi2_2sigma']: bf = 'D1_TENSION_2_TO_5_SIGMA'
    else: bf = 'D1_NOT_DISTINGUISHED'
    if reasons or not (isinstance(beta_med, float) and isinstance(beta_sig, float) and beta_sig > 0):
        mc = 'INCONCLUSIVE_SYSTEMATICS'
    else:
        zt = abs(beta_med - bt) / beta_sig
        if zt > 5.0: mc = 'D1_BETA_FALSIFIED'
        elif beta_sig > bt: mc = 'D1_BETA_INCAPAZ'
        elif beta_sig <= bt / 2.0 and zt <= 3.0: mc = 'D1_BETA_NOT_FALSIFIED_POWERED'
        elif zt > 3.0: mc = 'D1_BETA_TENSION'
        else: mc = 'D1_BETA_INCONCLUSIVE'
    for v in (bf, mc):
        assert 'CONFIRM' not in v and 'PROVED' not in v
    return bf, mc, reasons


def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def modo_injecao(nproc, K):
    from multiprocessing import Pool
    import camb, scipy
    t0 = time.time(); bt = beta_tgl()
    configs = [dict(nome='primario_C0_sem_SH0ES', usar_sh0es=False, livre_c=False, betas=[0.0, bt, -0.017], K=K),
               dict(nome='variante_com_SH0ES', usar_sh0es=True, livre_c=False, betas=[bt], K=max(12, K // 2)),
               dict(nome='sensibilidade_C_livre', usar_sh0es=False, livre_c=True, betas=[bt], K=max(12, K // 2))]
    rel = dict(versao='D1_CAMB_V3_PIPELINE_INJECAO', protocolo=PROTOCOLO_V3, executado=time.strftime('%Y-%m-%dT%H:%M:%S'),
               beta_TGL_runtime=bt, fiducial=FIDUCIAL.tolist(), criterios=CRITERIOS, limites=LIMITES,
               scripts=dict(worker=dict(path=W.__file__, sha256=sha256(W.__file__)), pipeline=dict(path=os.path.abspath(__file__), sha256=sha256(os.path.abspath(__file__)))),
               instrumento=dict(camb=camb.__version__, scipy=scipy.__version__, numpy=np.__version__, python=sys.version.split()[0]),
               valores_centrais_reais_lidos=False, configs=[])
    with Pool(nproc) as pool:
        for cfg in configs:
            for b in cfg['betas']:
                th = FIDUCIAL.copy(); th[3] = b
                asimov, dinj = dados_sinteticos(th, None, cfg['livre_c'])
                x0 = np.array(FIDUCIAL, float); x0[0] += 0.8; x0[2] += 0.002
                bf = ajuste(asimov, cfg['usar_sh0es'], livre_c=cfg['livre_c'], x0=x0)
                sig_a = sigma_fisher(bf['theta'], asimov, cfg['usar_sh0es'], bf['livres'])
                reals = []
                for _r in pool.imap_unordered(_uma_realizacao, [(th.tolist(), 1000 + s_, cfg['usar_sh0es'], cfg['livre_c']) for s_ in range(cfg['K'])]):
                    reals.append(_r)
                reals.sort(key=lambda r_: r_['semente'])
                ok = [r for r in reals if r['sigma'] and np.isfinite(r['chi2'])]
                pulls = np.array([(r['beta_hat'] - b) / r['sigma'] for r in ok])
                n_dados = 3 + len(DESI_ROWS) + (1 if cfg['usar_sh0es'] else 0)
                chis = np.array([r['chi2'] for r in ok])
                sc = [abs(r['selfcheck'] - 1) for r in ok if r['selfcheck'] is not None]
                item = dict(config=cfg['nome'], beta_injetado=b, asimov=dict(beta_hat=bf['theta'][3], sigma_fisher=sig_a, chi2=bf['chi2'],
                                                                             vies_em_sigma=(bf['theta'][3] - b) / sig_a, selfcheck=bf['selfcheck'],
                                                                             residuo_segunda=bf['residuo_segunda'], fecho_E0=bf['fecho_E0']),
                            K=cfg['K'], K_validos=len(ok), pull_media=float(pulls.mean()), pull_desvio=float(pulls.std(ddof=1)),
                            cobertura_1sigma=float(np.mean(np.abs(pulls) <= 1.0)), sigma_mediana=float(np.median([r['sigma'] for r in ok])),
                            chi2_medio=float(chis.mean()), n_dados=n_dados, n_livres=len(bf['livres']), selfcheck_pior=float(max(sc)) if sc else None,
                            realizacoes=reals)
                K2 = len(ok)
                item['checks'] = [
                    ('autoverificação β = 0 vs CAMB relida em todas as realizações (|razão − 1| < 5e-3)', bool(sc and max(sc) < CRITERIOS['selfcheck_tol'])),
                    ('Asimov: |β̂ − β_inj| < 0,1 σ', bool(abs(item['asimov']['vies_em_sigma']) < 0.1)),
                    ('Asimov: χ² ≈ 0 (< 1e-3)', bool(bf['chi2'] < 1e-3)),
                    ('fecho H(0) = H0 e segunda equação na melhor solução', bool(abs(bf['fecho_E0'] - 1) < 1e-8 and bf['residuo_segunda'] < 1e-6)),
                    ('pull médio compatível com zero (|média| < 3/√K)', bool(abs(item['pull_media']) < 3.0 / np.sqrt(K2))),
                    ('desvio dos pulls em [0,7; 1,3]', bool(0.7 <= item['pull_desvio'] <= 1.3)),
                    ('todas as realizações ajustadas', bool(K2 == cfg['K']))]
                item['todos'] = all(v for _, v in item['checks'])
                rel['configs'].append(item)
                print('%-28s β_inj=%+.5f  Asimov β̂=%+.6f σ=%.5f viés=%.3fσ | K=%d pull %.3f±%.3f cobertura %.2f σ_med %.5f χ²méd %.2f (n-p=%d) sc %.1e -> %s'
                      % (cfg['nome'], b, bf['theta'][3], sig_a, item['asimov']['vies_em_sigma'], K2, item['pull_media'], item['pull_desvio'],
                         item['cobertura_1sigma'], item['sigma_mediana'], item['chi2_medio'], n_dados - len(bf['livres']), item['selfcheck_pior'] or -1,
                         'OK' if item['todos'] else 'FALHOU'), flush=True)
    # validação do caminho da fase 3 (MCMC) em dados SINTÉTICOS sem ruído (β_TGL injetado, primário)
    th = FIDUCIAL.copy(); th[3] = bt
    asimov, _ = dados_sinteticos(th, None, False)
    mc = fase3_mcmc(asimov, False, False, nproc)
    sb = mc['summary']['beta']; sig_mc = 0.5 * (sb['sigma_lower'] + sb['sigma_upper'])
    sig_f = next(c['asimov']['sigma_fisher'] for c in rel['configs'] if c['config'] == 'primario_C0_sem_SH0ES' and abs(c['beta_injetado'] - bt) < 1e-12)
    bf_, mc_, rs_ = matriz_v2(0.0, 0.0, 15, [1.0], sb['median'], sig_mc)
    rel['mcmc_asimov'] = dict(resultado=mc, sigma_mcmc=sig_mc, sigma_fisher=sig_f, desvio_mediana_em_sigma=(sb['median'] - bt) / sig_mc,
                              matriz_v2_no_asimov=[bf_, mc_, rs_],
                              checks=[('MCMC em Asimov: mediana de β a menos de 0,3 σ da injeção', bool(abs(sb['median'] - bt) / sig_mc < 0.3)),
                                      ('MCMC em Asimov: σ(β) do MCMC a menos de 30% da σ de Fisher', bool(abs(sig_mc / sig_f - 1) < 0.3)),
                                      ('MCMC em Asimov: aceitação entre 0,1 e 0,7', bool(0.1 <= mc['acceptance_fraction_mean'] <= 0.7))])
    rel['mcmc_asimov']['todos'] = all(v for _, v in rel['mcmc_asimov']['checks'])
    print('MCMC Asimov: β = %.5f +%.5f −%.5f (σ %.5f; Fisher %.5f); aceitação %.3f; %s' % (sb['median'], sb['sigma_upper'], sb['sigma_lower'], sig_mc, sig_f,
          mc['acceptance_fraction_mean'], 'OK' if rel['mcmc_asimov']['todos'] else 'FALHOU'), flush=True)
    rel['todos'] = all(c['todos'] for c in rel['configs']) and rel['mcmc_asimov']['todos']
    rel['veredito'] = ('D1_V3_PIPELINE_VALIDATED_BY_INJECTION__REAL_DATA_LOCKED__AWAITING_OPERATOR_ONE_LINE_CONFIRMATION' if rel['todos']
                       else 'D1_V3_PIPELINE_INJECTION_FAILED__NOT_READY')
    rel['runtime_s'] = time.time() - t0
    out = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_INJECAO.json'); os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + '.tmp'; json.dump(rel, open(tmp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str); os.replace(tmp, out)
    print('veredito:', rel['veredito'], '| %.0fs' % rel['runtime_s'], '->', out)


def modo_real():
    conf = os.path.join(AQUI, 'CONFIRMACAO_OPERADOR_ROTA_V3.json')
    motivo = None
    if not os.path.exists(conf):
        motivo = 'arquivo de confirmação ausente'
    else:
        c = json.load(open(conf, encoding='utf-8'))
        linha = (c.get('linha_do_operador') or '').strip()
        if c.get('protocolo') != PROTOCOLO_V3: motivo = 'protocolo divergente'
        elif not linha: motivo = 'linha do operador vazia'
        elif c.get('sha256_linha') != hashlib.sha256(linha.encode('utf-8')).hexdigest(): motivo = 'hash da linha não confere'
    if motivo:
        out = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_REAL_RECUSADO.json'); os.makedirs(os.path.dirname(out), exist_ok=True)
        json.dump(dict(veredito='D1_V3_REAL_DATA_REFUSED__OPERATOR_CONFIRMATION_MISSING', motivo=motivo, protocolo=PROTOCOLO_V3,
                       quando=time.strftime('%Y-%m-%dT%H:%M:%S')), open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print('RECUSADO:', motivo); sys.exit(3)
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    dados = _dados_reais(); dados['livre_c'] = False; bt = beta_tgl(); t0 = time.time()
    out = dict(versao='D1_CAMB_V3_REAL', protocolo=PROTOCOLO_V3, confirmacao=json.load(open(conf, encoding='utf-8')), executado=time.strftime('%Y-%m-%dT%H:%M:%S'),
               scripts=dict(worker=sha256(W.__file__), pipeline=sha256(os.path.abspath(__file__))), fases={})
    l1 = ajuste(dados, False, beta_fixo=0.0); t1 = ajuste(dados, False, beta_fixo=bt)
    out['fases']['fase1_primario'] = dict(LCDM=l1, TGL=t1, delta_chi2=t1['chi2'] - l1['chi2'], n_dados=15)
    l1s = ajuste(dados, True, beta_fixo=0.0); t1s = ajuste(dados, True, beta_fixo=bt)
    out['fases']['fase1_variante_SH0ES'] = dict(LCDM=l1s, TGL=t1s, delta_chi2=t1s['chi2'] - l1s['chi2'], n_dados=16)
    out['fases']['fase2_H0'] = dict(H0_LCDM=l1['theta'][0], H0_TGL=t1['theta'][0], tensao_LCDM_sigma=abs(l1['theta'][0] - dados['sh0es_mean']) / SH0ES_SIGMA,
                                     tensao_TGL_sigma=abs(t1['theta'][0] - dados['sh0es_mean']) / SH0ES_SIGMA)
    m3 = fase3_mcmc(dados, False, False, nproc); m3c = fase3_mcmc(dados, False, True, nproc)
    out['fases']['fase3_mcmc_primario'] = m3; out['fases']['fase3_mcmc_C_livre'] = m3c
    sb = m3['summary']['beta']; sg = 0.5 * (sb['sigma_lower'] + sb['sigma_upper'])
    bf, mc, reasons = matriz_v2(out['fases']['fase1_primario']['delta_chi2'], l1['chi2'], 15, [l1['selfcheck'], t1['selfcheck']], sb['median'], sg)
    out.update(bestfit_outcome=bf, mcmc_outcome=mc, reasons=reasons, runtime_s=round(time.time() - t0, 1),
               veredito='TGL_D1_CAMB_V3__BESTFIT_%s__MCMC_%s' % (bf, mc))
    p = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_REAL_RESULT.json'); tmp = p + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str); os.replace(tmp, p)
    print(out['veredito'], '->', p)


def modo_autoverificacao():
    bt = beta_tgl(); linhas = []
    for b in (0.0, bt, -0.017):
        for c in (0.0, 0.01):
            d = W.derivados(dict(beta=b, H0=67.5, ombh2=0.02237, omch2=0.12, c=c, desi_z=DESI_Z))
            linhas.append(dict(beta=b, c=c, selfcheck=d['dm_selfcheck_ratio'], E0=d['E_at_z0'], residuo_segunda=d['second_friedmann_residual'],
                               Phi_z0=d['Phi_z0'], P_sobre_rho_zstar=d['P_over_rho_zstar'], R=d['R'], lA=d['lA'], r_drag=d['r_drag_TGL'], Omega_L=d['Omega_L']))
    f = W.FundoV3(67.5, 0.02237, 0.12, 0.02)
    lim = []
    for zz in (1e7, 30.0):
        i = int(np.argmin(np.abs(f.x + np.log1p(zz)))); lim.append(dict(z=zz, P_sobre_rho=float((f.E2[i] - f.c) / f.rho[i])))
    checks = [('β = 0: |DM/DM_CAMB − 1| < 5e-3', all(abs(l['selfcheck'] - 1) < 5e-3 for l in linhas)),
              ('fecho H(0) = H0 (|E0 − 1| < 1e-8) em todos os casos', all(abs(l['E0'] - 1) < 1e-8 for l in linhas)),
              ('segunda equação d(E²)/du + 3Φ(ρ+p) = 0 (resíduo < 1e-6)', all(l['residuo_segunda'] < 1e-6 for l in linhas)),
              ('limite da radiação: P/ρ → 1 + 4β/3 (β = 0,02)', abs(lim[0]['P_sobre_rho'] - (1 + 4 * 0.02 / 3)) < 1e-4),
              ('limite da matéria: P/ρ → 1 + β (β = 0,02, z = 30; tolerância 1e-3)', abs(lim[1]['P_sobre_rho'] - 1.02) < 1e-3)]
    rel = dict(versao='D1_CAMB_V3_AUTOVERIFICACAO', protocolo=PROTOCOLO_V3, beta_TGL_runtime=bt, casos=linhas, limites_w_constante=lim,
               checks=checks, todos=all(v for _, v in checks))
    out = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_AUTOVERIFICACAO.json'); os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(rel, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    for n, v in checks: print(('OK   ' if v else 'FALHA'), n)
    print('todos:', rel['todos'])


if __name__ == '__main__':
    modo = sys.argv[1] if len(sys.argv) > 1 else 'autoverificacao'
    if modo == 'autoverificacao': modo_autoverificacao()
    elif modo == 'injecao': modo_injecao(int(sys.argv[2]) if len(sys.argv) > 2 else 40, int(sys.argv[3]) if len(sys.argv) > 3 else 48)
    elif modo == 'real': modo_real()
    else: raise SystemExit('modo desconhecido')
