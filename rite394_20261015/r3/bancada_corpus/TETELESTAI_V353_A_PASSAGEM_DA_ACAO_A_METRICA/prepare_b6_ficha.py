from pathlib import Path
import re,hashlib,json,datetime,os
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/AuditPassageScope.lean').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
rows=[]
items={'TGLExt/TheImportedEquilibrium':['the_trio_is_a_pair','the_pair_still_needs_its_hypotheses','discharge_by_import'],
 'TGL/AreaScale':['newtonPlanck_equivalence','halfNat_over_two_faces_eq_quarter'],
 'TGLExt/SectorFluidClosure':['SectorFluid'],
 'TGLExt/ThermodynamicFriedmann':['HubbleHorizonInput','variable_entropy_derivative'],
 'TGLExt/SectorRouteComparison':['the_two_routes_equal_iff','zero_flux_has_no_unique_factor']}
for stem,names in items.items():
    p=R/'kernel'/f'{stem}.lean';s=p.read_text(encoding='utf8')
    for n in names:
        m=re.search(r'^(?:structure|theorem) '+n+r'\b',s,re.M);assert m,n
        end=s.find('where' if s[m.start():].startswith('structure') else ':=',m.start())
        rows.append(dict(name=n,path=str(p),line=s[:m.start()].count('\n')+1,sha256=sha(p),statement=s[m.start():end].strip(),decision='REUSAR sem novo teorema; auditar os fornecedores de estatuto'))
anchors=['EXTERNAL_KNOWN_THEOREMS =','def prove_d1_camb_protocol(']
cons=[dict(path=str(R/'um.py'),line=i+1,text=l.strip(),sha256=sha(R/'um.py')) for i,l in enumerate((R/'um.py').read_text(encoding='utf8').splitlines()) if any(a in l for a in anchors)]
target='''B6 adds no mathematical assertion or axiom. Deliver typed JSON proposal:
 external_known_theorems: four entries with name,status,citation,exact_role,verified_url,
 source_read_scope,imported_into_witness=false;
 scope: H3 IMPORTED (conditional modus ponens), G/eta INPUT, H_nx INPUT,
 modified differential entropy INPUT, global Lemma3 OPEN, TGL-S/TGL-L OPEN;
 corrections: radius in Cai-Kim flux, variable-Phi derivative, density support for equality,
 nonzero total enthalpy for unique Phi_flux, explicit cosmological/integration constant;
 changes_gate=false, implements_runtime=false, chooses_route=false.
Audit existing fullnames by Lake: TheImportedEquilibrium logical providers, AreaScale calibration,
SectorFluid H_nx structure, HubbleHorizonInput, B4 derivative/support conditions.
No new theorem is needed for a bibliography or status table; importing a theorem as an implication
does not construct its horizon/equilibrium premise. The four literature sources do not prove Phi_TGL.'''
order=R.parent/'TUNEL/PARA_CHATGPT/ORDEM_012_a_passagem_da_acao_a_metrica.md'
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DOS_ARTEFATOS_B6',target=target,decision='REUSAR e documentar: nenhum teorema novo; somente auditor de fornecedores existentes e propostas documentais tipadas.',providers=rows,consumers=cons,order=dict(path=str(order),sha256=sha(order)),searches=[json.loads((R/p).read_text(encoding='utf8')) for p in ['BUSCAS_B6.json','BUSCAS_B6_RETRY.json']],limits=['Buscas por nomes/tipos e recortes, não varredura exaustiva de todo conteúdo.','Gibbons–Hawking: metadados e resumo oficiais lidos; PDF oficial retornou 401. Não alegar leitura integral.','Cai–Kim: seção2 lida em HTML primário, incluindo raio, fluxo, temperatura e conservação. Jacobson: texto primário lido sobre horizontes locais/hipóteses. Padmanabhan: resumo e trechos introdutórios primários lidos, papel contextual.','Não alterar EXTERNAL_KNOWN_THEOREMS canônico: gerar proposta para gerência.','Não derivar H3, G ou lei Phi por mera citação. B6 não encerra A1(b), que retoma após as entregas B1–B6.'])
put(R/'REAPROVEITAMENTO_B6.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior aos artefatos B6]\n\n# B6 — estatutos e importações explícitas\n\n'+data['decision']+'\n\n## Tipo do produto\n```text\n'+target+'\n```\n\n## Consumidores\n```json\n'+json.dumps(cons,ensure_ascii=False,indent=2)+'\n```\n\n## Fornecedores\n'
for r in rows:md+=f"\n### {r['name']}\n{r['path']}:{r['line']} · SHA256 `{r['sha256']}`\n```lean\n{r['statement']}\n```\n{r['decision']}\n"
md+='\n## Buscas\n```json\n'+json.dumps(data['searches'],ensure_ascii=False,indent=2)+'\n```\n\n'+'\n'.join('- '+x for x in data['limits'])+'\n\n'+data['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B6.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(rows),consumers=len(cons))))
