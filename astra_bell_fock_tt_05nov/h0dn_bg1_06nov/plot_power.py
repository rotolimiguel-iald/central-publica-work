"""Plot frozen-score distributions after label release, without model changes."""
from pathlib import Path
import json, numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
r=json.loads((BASE/'blind_custodian/UNBLINDED_RESULTS.json').read_text('utf-8'))
rows=json.loads((BASE/'blind_custodian/SCORES_MANIFEST.json').read_text('utf-8'))
case=next(c for c in r['outputs'] if c['kind']=='ordinary' and c['hypothesis']==1 and c['fixed_bias']==0 and c['random_sd']==0)
zs=[]
for row in rows:
    if row['case_id']==case['id']:
        with np.load(row['score_path']) as d:zs.append(d['z_null'])
z=np.concatenate(zs)
fig,axes=plt.subplots(1,2,figsize=(11,4.4),layout='constrained')
colors=['#1461a8','#c46217'];labels=['Rede publicada','Viés de Cefeidas livre']
x=np.linspace(1,11,800)
for i,ax in enumerate(axes):
    m=case['models'][i];D=m['prediction_mean_Z'];p=m['rejection']['estimate']
    ax.hist(z[:,i],bins=75,range=(1,11),density=True,color=colors[i],alpha=.28,label='Injeções cegas')
    ax.plot(x,norm.pdf(x-D),color=colors[i],lw=2,label='Previsão gaussiana')
    ax.fill_between(x,0,norm.pdf(x-D),where=x>=5,color=colors[i],alpha=.16)
    ax.axvline(5,color='#333333',ls='--',lw=1.5,label='Limiar 5σ')
    ax.set_title(labels[i],fontweight='bold');ax.set_xlim(1,11);ax.set_ylim(0,.46)
    ax.set_xlabel('Escore contra desvio zero (Z)');ax.set_ylabel('Densidade')
    ax.text(.97,.95,f'D esperado = {D:.2f}σ\nP(Z ≥ 5) = {100*p:.2f}%',transform=ax.transAxes,ha='right',va='top',fontsize=11)
    ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False)
    ax.legend(frameon=False,loc='upper left',fontsize=8)
fig.suptitle('H0DN × BG1 — poder prospectivo, 100.000 injeções TGL',fontsize=14,fontweight='bold')
fig.supxlabel('Covariância publicada; aproximação gaussiana. Correlações adicionais entre degraus permanecem abertas.',fontsize=9)
out=BASE/'PODER_CEGO.png'
if out.exists():raise FileExistsError(out)
fig.savefig(out,dpi=170)
print(out)
