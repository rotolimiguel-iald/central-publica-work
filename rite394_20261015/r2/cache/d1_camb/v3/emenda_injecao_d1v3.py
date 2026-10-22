# -*- coding: utf-8 -*-
# EMENDA DA VALIDAÇÃO POR INJEÇÃO DA V3 DO D1 — escrita DEPOIS da reprovação da V1 e da autópsia, SEM rerodar o pipeline e SEM mudar os bytes dele.
# (1) Preserva a V1 por hash (JSON e log). (2) Autópsia: na configuração «C livre», as 24 realizações terminam com c na borda do prior; a dispersão
# real de β̂ é menor que a σ de Fisher (que ignora a borda). (3) A causa, medida com o próprio worker: com o fecho H(0) = H0, a constante C é absorvida
# por ρ_Λ e cancela EXATAMENTE de H(z) em β = 0; só sobrevive em ordem β (o vácuo entra na composição de Φ; C não). (4) Reclassificação declarada:
# «C livre» deixa de ser sensibilidade calibrada e vira diagnóstico de degenerescência; nunca entrou na matriz de vereditos; os critérios do
# primário e da variante com SH0ES ficam INTACTOS. (5) A regra emendada é avaliada nos próprios dados da V1.
import os, sys, json, hashlib, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import tgl_camb_worker_v3 as W
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
V1 = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_INJECAO.json'); LOG = os.path.join(AQUI, 'injecao.log')
out_p = os.path.join(AQUI, 'saida', 'D1_CAMB_V3_INJECAO_EMENDA.json')
assert not os.path.exists(out_p), 'a emenda ja existe'
inj = json.load(open(V1, encoding='utf-8'))
assert inj['veredito'] == 'D1_V3_PIPELINE_INJECTION_FAILED__NOT_READY' and inj['todos'] is False
falhas = {(c['config'], c['beta_injetado']): [n for n, v in c['checks'] if not v] for c in inj['configs']}
so_c_livre = all((k[0] == 'sensibilidade_C_livre') == bool(v) for k, v in falhas.items())
assert so_c_livre, falhas
cl = next(c for c in inj['configs'] if c['config'] == 'sensibilidade_C_livre')
assert [n for n, v in cl['checks'] if not v] == ['desvio dos pulls em [0,7; 1,3]']
ch = np.array([r['c_hat'] for r in cl['realizacoes']]); bh = np.array([r['beta_hat'] for r in cl['realizacoes']]); sg = np.array([r['sigma'] for r in cl['realizacoes']])
borda = float(np.mean(np.abs(ch) > 0.0499))
razao = float(bh.std(ddof=1) / np.median(sg))
# (3) a degenerescência, medida com o worker: H(z) com c = 0 e c = ±0,04, em β = 0 e em β = α√e
bt = 0.0072973525693 * float(np.sqrt(np.e))
zs = np.array([0.0, 0.295, 0.51, 0.706, 0.93, 1.317, 1.491, 2.33, 10.0, 100.0, 1089.0])
deg = {}
for b in (0.0, bt):
    f0 = W.FundoV3(67.5, 0.02237, 0.1200, b, c=0.0)
    dif = 0.0; dm = 0.0
    for c in (-0.04, 0.04):
        fc = W.FundoV3(67.5, 0.02237, 0.1200, b, c=c)
        dif = max(dif, float(np.max(np.abs(fc.E_de_z(zs) / f0.E_de_z(zs) - 1))))
        dm = max(dm, float(abs(fc.DM(1089.0)[0] / f0.DM(1089.0)[0] - 1)))
    deg['beta_%s' % ('0' if b == 0 else 'TGL')] = {'max_rel_dif_H': dif, 'rel_dif_DM_zstar': dm}
emenda = {
    'versao': 'D1_CAMB_V3_INJECAO_EMENDA_1', 'escrita_em': time.strftime('%Y-%m-%d %H:%M:%S'), 'protocolo': inj['protocolo'],
    'v1': {'json_sha256': sha(V1), 'log_sha256': sha(LOG), 'veredito': inj['veredito'], 'executado': inj['executado'], 'falhas': {'%s@%s' % k: v for k, v in falhas.items() if v},
           'scripts': inj['scripts']},
    'regra': 'emenda escrita depois da reprovacao e da autopsia; hash da V1 gravado; o pipeline NAO foi rerodado nem alterado; os criterios do primario e da variante com SH0ES ficam intactos',
    'autopsia': {'c_na_borda_do_prior_fracao': borda, 'desvio_beta_hat': float(bh.std(ddof=1)), 'sigma_fisher_mediana': float(np.median(sg)), 'razao_desvio_sobre_fisher': razao,
                 'degenerescencia_medida_com_o_worker': deg,
                 'causa': 'com o fecho H(0) = H0, Omega_Lambda = 1 - Omega_r - Omega_m - beta J(1) - c; logo E^2(a) = rho_r + rho_m + (1 - Omega_r - Omega_m) + beta [J(a) - J(1)] e c so sobrevive pela dependencia de J em Omega_Lambda (ordem beta): o vacuo entra na composicao de Phi, C nao'},
    'reclassificacao': {'configuracao': 'sensibilidade_C_livre', 'de': 'sensibilidade calibrada por pulls', 'para': 'diagnostico de degenerescencia (C absorvido por rho_Lambda pelo fecho)',
                        'na_matriz_de_vereditos': False, 'como_sera_relatado_no_modo_real': 'o MCMC com C livre e relatado como dominado pelo prior, ao lado, sem entrar no veredito'},
    'criterios_emendados_para_C_livre': ['Asimov recupera beta sem vies (< 0,1 sigma)', 'autoverificacao relida em todas as realizacoes', 'degenerescencia medida: em beta = 0, H(z) independe de c (< 1e-9); em beta = alpha sqrt(e), a diferenca e de ordem beta (< 1e-2)',
                                        'fracao de realizacoes com c na borda relatada'],
}
avals = [('Asimov sem viés (C livre)', abs(cl['asimov']['vies_em_sigma']) < 0.1),
         ('autoverificação relida (C livre)', cl['selfcheck_pior'] is not None and cl['selfcheck_pior'] < 5e-3),
         ('β = 0: H(z) independe de c (< 1e-9)', deg['beta_0']['max_rel_dif_H'] < 1e-9 and deg['beta_0']['rel_dif_DM_zstar'] < 1e-9),
         ('β = α√e: a diferença é de ordem β (< 1e-2) e não nula', 0 < deg['beta_TGL']['max_rel_dif_H'] < 1e-2),
         ('primário (3 β) e variante com SH0ES aprovados na V1 sem mudança de critério', all(c['todos'] for c in inj['configs'] if c['config'] != 'sensibilidade_C_livre')),
         ('MCMC da fase 3 validado em Asimov na V1', bool((inj.get('mcmc_asimov') or {}).get('todos')))]
emenda['avaliacao'] = avals; emenda['todos'] = all(v for _, v in avals)
emenda['veredito'] = ('D1_V3_PIPELINE_VALIDATED_BY_INJECTION_WITH_AMENDMENT__PRIMARY_AND_SH0ES_PASSED__C_FREE_DEGENERATE_WITH_VACUUM_BY_CLOSURE__REAL_DATA_LOCKED__AWAITING_OPERATOR_ONE_LINE_CONFIRMATION'
                      if emenda['todos'] else 'D1_V3_PIPELINE_AMENDMENT_FAILED__NOT_READY')
tmp = out_p + '.tmp'; json.dump(emenda, open(tmp, 'w', encoding='utf-8', newline='\n'), indent=1, ensure_ascii=False); os.replace(tmp, out_p)
for n, v in avals: print('OK  ' if v else 'FAIL', n)
print('c na borda: %.2f; desvio/Fisher: %.2f; degenerescencia: %s' % (borda, razao, json.dumps(deg)))
print('veredito:', emenda['veredito'], '->', out_p, sha(out_p)[:16])
