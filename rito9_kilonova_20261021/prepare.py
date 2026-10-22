"""Immutable local custody and preregistration; no imports from scientific originals."""
from pathlib import Path
import hashlib, json, re
from datetime import datetime, timezone

B = Path(__file__).resolve().parent
S = Path(r'C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg')
U = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
def sha(data): return hashlib.sha256(data).hexdigest()
def save(name, obj):
    with (B/name).open('x', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)

names = ['HANDOFF_PARA_CHATGPT_20261021.md', 'PRE_REGISTRO_RITO9_KILONOVA.md',
 'DERIVACAO_ELO1_RITO9.md','FECHO_ELO1_E_ARVORE_ELO3.md',
 'DERIVACAO_POTENCIA_DT_NU.md','DERIVACAO_M1_PRIMEIRA_LEI.md',
 'pedras_candidatas/SeletorGeneralizado.lean','ferramentas/verifica_seletor_generalizado.py']
sources=[]
for name in names:
    data=(S/name).read_bytes(); out=B/'sources'/name; out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('xb') as f: f.write(data)
    sources.append(dict(original=str(S/name),copy=str(out),bytes=len(data),sha256=sha(data)))
data=U.read_bytes()
m=re.search(rb'^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)\r?$',data,re.M)
if not m: raise RuntimeError('Missing unique top-level alpha assignment')
save('CUSTODY_R1.json',dict(sources=sources,um=dict(path=str(U),sha256=sha(data),bytes=len(data)),
    alpha_source=dict(line=data[:m.start()].count(b'\n')+1,assignment=m.group().decode(),value=float(m[1])),
    scope='bytes read only; source presence is not a new custody seal or execution'))
save('PREREG_SYNTHETIC_R1.json',dict(created_utc=datetime.now(timezone.utc).isoformat(),
    scope='Synthetic diagnostic, NOT observational preregistration or measured significance',
    reused_route='d7.kilonova_fronteira_aguda; seq1305/1307/1309/1311',
    nos_query='F1.RITO9_KN_20261021 absent from current graph; source and map consulted directly',
    beta='alpha extracted from um.py * sqrt(e), runtime', c_m_s=299792458,
    lengths_km=[10,20,30],length_statute='INPUT exploratory, not inferred from a BNS',
    model='N geometric(p=beta) on 1,2,...; total=N*l/c; excess=(N-1)*l/c',
    quantiles=[0.05,0.5,0.95],seed=20261021,mc_samples=200000,
    tolerances=dict(algebra_abs=1e-12,mc_mean_relative=0.02,mc_sd_relative=0.02),
    checks=['geometric moments against deterministic seeded simulation',
     'quantiles satisfy exact discrete CDF bracket',
     'excess subtracts one free crossing',
     'equal mean delays in GW and neutrinos cancel in mean difference, not necessarily fluctuations',
     'arbitrary projector angles satisfy selector; identity commutes for all angles',
     'constant mixing angle does not remove an energy-dependent phase delay',
     'changing l and beta proportionally preserves mean, not full discrete distribution',
     'first detected packet is not sample mean; minimum of m independent waits has different law'],
    prohibitions=['No observed event data','No fitted parameters','No sigma claim from MC sample size',
                  'No kernel/um.py/production writes','No infrastructure instructions executed'],
    expected_report='analytic and synthetic results with hypotheses, instrumental feasibility and unresolved physical mapping'))
print('Custody and synthetic preregistration saved before test execution')
