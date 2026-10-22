# DIAGNOSTICO NAO-CEGO da gerencia (22/09/2026): a consistencia da probabilidade conjunta V2
# refeita trocando o canal D1 V2 (superado) pelo D1 V3 real (v366). Tudo lido do core por script.
import json, math, hashlib
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
b = open(P, 'rb').read(); c = json.loads(b)['core']
beta = c['joint_coincidence_result_v2']['beta_runtime']
chk = 0.0072973525693 * math.sqrt(math.e)  # CODATA 2018 alpha * sqrt(e), so conferencia
out = {"core_sha16": hashlib.sha256(b).hexdigest()[:16], "beta_runtime_lido": beta, "beta_recalc_minus_lido": chk - beta}
zs = {z['id']: z['z'] for z in c['joint_coincidence_result_v2']['consistency']}
out['z_v2_lidos'] = zs
v3 = c['d1_camb_v3_real_v366']['beta_posterior']
z_v3_sym = (v3['median'] - beta) / v3['sigma']
z_v3_up = (v3['median'] - beta) / v3['sigma_upper']
out['z_d1_v3_simetrico'] = z_v3_sym; out['z_d1_v3_sigma_superior'] = z_v3_up
out['z_d1_v3_core'] = c['d1_camb_v3_real_v366']['z_alpha_sqrt_e']
zs2 = dict(zs); zs2.pop('d1_camb_v2_beta'); zs2['d1_camb_v3_beta'] = z_v3_sym
m = max(abs(v) for v in zs2.values())
out['max_abs_z_com_v3'] = m; out['consistent_com_v3_(z<3)'] = m < 3.0
out['canal_que_domina'] = max(zs2, key=lambda k: abs(zs2[k]))
out['P_all_primario_inalterado'] = c['joint_coincidence_result_v2']['primary']['P_all']
out['nota'] = "D1 nao e canal 'detectado' (sinal oposto) => P_all nao muda; so a consistencia muda de z=3.86 para ~3.01 (no limiar 3)."
json.dump(out, open('recompute_joint_v3.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
