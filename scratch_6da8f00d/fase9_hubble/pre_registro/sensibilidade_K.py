import json,sys,os,re,math
sys.stdout.reconfigure(encoding='utf-8')
NOS=r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
src=open(os.path.join(NOS,'um.py'),'rb').read().decode('utf-8','replace')
alpha=float(re.search(r'ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',src).group(1))
beta=alpha*math.sqrt(math.e)
core=json.load(open(os.path.join(NOS,'um_absoluto.json'),encoding='utf-8'))['core']
d=core['the_dissipation_law_with_contrast_v378']
Om=d['Omega_m']; Or=d['Omega_r']; OL=d['Omega_L']; zs=d['z_star_input']
def E(z,Om,Or,OL): return math.sqrt(Om*(1+z)**3+Or*(1+z)**4+OL)
def K(Om,Or,OL,zs): return E(zs,Om,Or,OL)**(2*beta/3)
K0=K(Om,Or,OL,zs)
out={'beta':beta,'Omega_m':Om,'Omega_r':Or,'Omega_L':OL,'z_star':zs,'E_zstar':E(zs,Om,Or,OL),'E_zstar_core':d['E_z_star'],'K_D1b':K0,'K_D1b_core':d['K_D1b_runtime']}
# sensibilidades
dOm=0.007
K1=K(Om+dOm,Or,OL-dOm,zs); out['dK_dOmega_m_0p007']=K1-K0
dz=0.3
K2=K(Om,Or,OL,zs+dz); out['dK_dzstar_0p3']=K2-K0
# fundo
H0bg=core['bancada_fase4_v378']['P_ladder_d1b']['H0_bg']; Kf=core['bancada_fase4_v378']['P_ladder_d1b']['K']
out['H0_bg_fase4']=H0bg; out['K_fase4']=Kf; out['H0_local_fase4']=core['bancada_fase4_v378']['P_ladder_d1b']['H0_local']
sig_bg=0.301  # Fd_lcdm_planck_dr2 sigma (Fase 3 prereg, Bancada) [REAL]
out['sigma_H0_bg_lcdm_planck_dr2_fase3']=sig_bg
out['sigma_H0_local_pred_from_bg']=Kf*sig_bg
out['H0_local_pred_planck2018']=67.36*K0
out['sigma_H0_local_pred_planck2018']=0.54*K0
# alvos [KNOWN - a ler] e z contra a previsao (ilustracao, nao veredito)
alvos={'SH0ES_R22':(73.04,1.04),'SH0ES_2025_JWST_cef':(73.49,0.93),'Riess_2024_JWST_3met':(72.6,2.0),'CCHP_2024_TRGB_JAGB':(70.39,1.936),'CCHP_TRGB_only':(68.81,2.224),'CCHP_JAGB_only':(67.8,2.72),'SBF_JWST_2025':(73.8,2.404),'masers_2020':(73.9,3.0),'TDCOSMO_2025':(71.6,3.6),'Planck2018':(67.36,0.54),'DESI_DR2_BBN_[a_ler]':(68.5,0.6)}
pred=out['H0_local_fase4']; spred=out['sigma_H0_local_pred_from_bg']
out['z_vs_pred_ilustracao']={}
for k,(h,s) in alvos.items():
    out['z_vs_pred_ilustracao'][k]={'H0':h,'sigma':s,'z_vs_K_H0bg':(h-pred)/math.sqrt(s*s+spred*spred),'z_vs_H0bg':(h-H0bg)/math.sqrt(s*s+sig_bg*sig_bg)}
# poder previo (o salto K-1 contra sigma do leitor)
for k,(h,s) in alvos.items():
    out['z_vs_pred_ilustracao'][k]['poder_previo_K_minus_1']=(Kf-1)*H0bg/math.sqrt(s*s+sig_bg*sig_bg*Kf*Kf)
# combinacao dos locais (ilustracao): SH0ES R22 + CCHP + SBF + masers + TDCOSMO (sem sirenes)
import itertools
sets={'A_so_sh0es':['SH0ES_R22'],'B_seis_sem_sirenes':['SH0ES_2025_JWST_cef','CCHP_2024_TRGB_JAGB','SBF_JWST_2025','masers_2020','TDCOSMO_2025'],'C_sem_cefeidas':['CCHP_2024_TRGB_JAGB','SBF_JWST_2025','masers_2020','TDCOSMO_2025']}
out['poder_previo_conjuntos']={}
for nm,ks in sets.items():
    w=sum(1/alvos[k][1]**2 for k in ks); sc=1/math.sqrt(w)
    out['poder_previo_conjuntos'][nm]={'sigma_comb':sc,'poder_K_minus_1':(Kf-1)*H0bg/math.sqrt(sc*sc+(sig_bg*Kf)**2)}
# K(z) dependencia em z para a lei acumulada (ilustracao): K(z)=exp(beta[I(z*)-I(z)]) com I=(2/3)ln E
def I(z): return (2/3)*math.log(E(z,Om,Or,OL))
out['K_z']={}
for z in [0.0,0.01,0.05,0.1,0.5,1.0,2.0]:
    out['K_z'][str(z)]=math.exp(beta*(I(zs)-I(z)))
json.dump(out,open('SENSIBILIDADE_K_E_PODER_PREVIO.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
print(json.dumps(out,indent=1,ensure_ascii=False))
