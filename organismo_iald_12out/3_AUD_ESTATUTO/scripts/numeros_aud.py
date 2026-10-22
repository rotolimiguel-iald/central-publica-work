# Conferencia independente dos numeros centrais das estrategias (sintetico; nenhum dado novo; beta em runtime)
import math, json, re
um = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
alpha=None
with open(um,"rb") as fh:
    for i,ln in enumerate(fh):
        m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", ln.rstrip(b"\r\n"))
        if m: alpha=float(m.group(1)); linha=i+1
beta = alpha*math.sqrt(math.e)
out={"alpha_linha":linha,"beta":beta}
# Fase 9 (numeros transcritos do core v391 pelas frentes; aqui so a algebra)
hl, sl = 72.8819, 0.9149      # media GLS dos leitores (core)
hb, sb = 68.531, 0.301        # fundo BG1
Ez = 22784.0                  # E(z*) fundo nu (frente B)
K = math.exp((2*beta/3)*math.log(Ez))
out["K_recomposto"]=K
def chi2min(Kmod): return (hl-Kmod*hb)**2/(sl**2+(Kmod*sb)**2)
zdisc = math.sqrt(chi2min(1.0)-chi2min(K)); out["z_disc_fundo_perfilado"]=zdisc
zdelta = (hl-K*hb)/math.sqrt(sl**2+(K*sb)**2); out["z_delta"]=zdelta
# sigma_local maxima para z_disc = 5 com o mesmo centro
def zd(sl_): return math.sqrt((hl-hb)**2/(sl_**2+sb**2)-(hl-K*hb)**2/(sl_**2+(K*sb)**2))
lo,hi=0.3,2.0
for _ in range(100):
    mid=(lo+hi)/2
    if zd(mid)>5: lo=mid
    else: hi=mid
out["sigma_local_max_para_5sigma"]=lo
# centro minimo para 5 sigma com sigma atual
def zdc(h): return math.sqrt((h-hb)**2/(sl**2+sb**2)-(h-K*hb)**2/(sl**2+(K*sb)**2)) if (h-hb)**2/(sl**2+sb**2)>(h-K*hb)**2/(sl**2+(K*sb)**2) else 0
lo,hi=70.0,74.274
for _ in range(100):
    mid=(lo+hi)/2
    if zdc(mid)<5: lo=mid
    else: hi=mid
out["centro_min_para_5sigma_sigma_GLS"]=hi
# Par K x N_eff
F=(7/8)*(4/11)**(4/3); NSM=3.044
dNeff=(4/3)*(1+F*NSM)/F*beta; lnK=(2*beta/3)*math.log(Ez)
out["Delta_Neff"]=dNeff; out["lnK"]=lnK; out["R_razao"]=dNeff/lnK; out["R_forma_fechada"]=2*(1+F*NSM)/(F*math.log(Ez))
out["quadratura_par_SO"]={s: math.sqrt(5.913**2+(dNeff/s)**2) for s in (0.055,0.050,0.045)}
out["sigma_Neff_para_5sigma"]=dNeff/5
out["nota"]="algebra sobre numeros transcritos do core pelas frentes (hl, sl, hb, sb, Ez); nenhum dado observado aberto; informativo, nao veredito"
json.dump(out, open(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_ESTATUTO\medidas\NUMEROS_AUD.json","w"), indent=1)
print(json.dumps(out, indent=1))
