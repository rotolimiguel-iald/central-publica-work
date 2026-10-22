# [DERIVED aqui, NAO-CEGO, aritmetica sobre campos do core v369] janela de tau* em que o Sr (Kim 2025) detectaria a 5 sigma sem ja exceder a cota de 95%
import json, hashlib
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
b = open(P,'rb').read(); c = json.loads(b)['core']['clock_test_result_v369']
sr = [p for p in c['P1']['platforms'] if p['id']=='sr87_kim2025'][0]
det = 5*sr['sigma_excess_per_s']/sr['Gamma_pred_per_s']
ub  = sr['Gamma_ub_per_s']/sr['Gamma_pred_per_s']
out = dict(core_sha16=hashlib.sha256(b).hexdigest()[:16], tau_star_para_5sigma_em_tP=det, tau_star_cota95_em_tP=ub, razao_janela=ub/det,
           ghz_N=c['five_sigma_requirement']['ghz_N_needed'], hbar_omega_eV=c['five_sigma_requirement']['hbar_omega_needed_eV_at_todays_sigma'])
json.dump(out, open('janela_relogio.json','w'), indent=1); print(out)
