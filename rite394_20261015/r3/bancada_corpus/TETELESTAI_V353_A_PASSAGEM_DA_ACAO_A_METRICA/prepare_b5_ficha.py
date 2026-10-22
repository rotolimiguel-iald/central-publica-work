from pathlib import Path
import re,hashlib,json,datetime,os
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/TheAngleReachesTheMetric.lean').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
rows=[]
for stem,names in {'SMatrix':['normSq_reflection'],'TheSameBetaReadsThreeFaces':['reflection_weight'],'ThermodynamicFriedmann':['entropyFactor','tgl_second_friedmann_from_clausius'],'SectorFriedmann':['tgl_friedmann_from_sector_closure']}.items():
    p=R/'kernel/TGLExt'/f'{stem}.lean';s=p.read_text(encoding='utf8')
    for n in names:
        m=re.search(r'^(?:def|theorem) '+n+r'\b',s,re.M);assert m,n
        rows.append(dict(name=n,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():s.find(':=',m.start())].strip(),decision='REUSAR literalmente; corolário por reescrita'))
anchors=['"ext_rp_hubble_form_kernel_proved":','def prove_d1_camb_protocol(','"ext_same_beta_reads_three_faces_kernel_proved":']
cons=[dict(path=str(R/'um.py'),line=i+1,text=l.strip(),sha256=sha(R/'um.py')) for i,l in enumerate((R/'um.py').read_text(encoding='utf8').splitlines()) if any(a in l for a in anchors)]
target='''c:TGLCoupling; theta=TGLExt.thetaMiguel c.beta, already defined.
coupling_eq_sin_sq: c.beta=(sin theta)^2 via actual reflection_weight and normSq_reflection.
the_angle_reaches_the_metric: entropyFactor c w=1+(sin theta)^2*abs(1+w).
the_passage: HubbleHorizonInput H t G (entropyFactor c w) E ->
 deriv H t=-4*pi*G*(1+(sin theta)^2*abs(1+w))*E.
the_angle_reads_sector_first: all B3 hypotheses unchanged (U open preconnected,
smooth positive a, finite H_nx sectors, totalrho>0, enthalpy>=0, G>0, H_null),
exists Lambda, H^2=(8*pi*G/3)*rho*(1+(sin theta)^2*abs(1+wEff))-Lambda/3.
No scalar, state, source, angle definition, differential law or horizon hypothesis added.'''
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO_B5',decision='REUSAR B1/B3/B4: somente corolários por reescrita; B5 não acrescenta conteúdo dinâmico.',target=target,providers=rows,consumers=cons,proposed_consumers=['ext_the_angle_reaches_the_metric_kernel_proved','ext_the_passage_kernel_proved'],searches=[json.loads((R/p).read_text(encoding='utf8')) for p in ['BUSCAS_B5.json','BUSCAS_B5_RETRY.json']],limits=['Nenhum theta, seno, cosseno ou raiz de beta é inserido em r_s, D_M, l_A ou worker H(z). Código Lean apenas lê as equações já obtidas.','A busca do índice do acervo tem corte declarado e majoritariamente registros de auditoria da matriz-S; não é prova de ausência exaustiva.','B1/B2 selados, B3 compilado/auditado, B4 compilado e auditor em curso. Não modificar fornecedores por esta ficha.','Λ, G e hipóteses de horizonte e não-troca conservam seus estatutos.'])
put(R/'REAPROVEITAMENTO_B5.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior ao código B5]\n\n# B5 — leitura angular, sem conteúdo dinâmico novo\n\n'+data['decision']+'\n\n## Tipo\n```text\n'+target+'\n```\n\n## Consumidores\n```json\n'+json.dumps(cons,ensure_ascii=False,indent=2)+'\n```\n\n## Fornecedores\n'
for r in rows:md+=f"\n### {r['name']}\n{r['path']}:{r['line']} · SHA256 `{r['sha256']}`\n```lean\n{r['statement']}\n```\n{r['decision']}\n"
md+='\n## Buscas\n```json\n'+json.dumps(data['searches'],ensure_ascii=False,indent=2)+'\n```\n\n'+'\n'.join('- '+x for x in data['limits'])+'\n\n'+data['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B5.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(rows),consumers=len(cons))))
