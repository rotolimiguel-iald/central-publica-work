from pathlib import Path
import datetime, hashlib, json, os, re
R=Path(__file__).resolve().parent
assert not (R/'kernel/TGLExt/TheSameBetaReadsThreeFaces.lean').exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,b):
    assert not p.exists(); q=p.with_name(p.name+'.tmp'); q.write_bytes(b)
    assert q.read_bytes()==b and len(b)>0; os.replace(q,p)
names={
 'TheVerbalCoupling':['thetaMiguel','sin_thetaMiguel','the_pruning_threshold_is_the_reflection_amplitude'],
 'SMatrix':['normSq_reflection','normSq_reflection_add_transmission'],
 'TheFiveHalves':['boundary_extracts_the_radical'],
 'TheGeometricCostOfAbsoluteZero':['the_minimal_volume_exceeds_one'],
 'RhoPlusPClosure':['closure_identity','hubble_form','the_background_closure'],
 'NoFullWitness':['leakage_strictly_loses','beta_forbids_full_static_witness','leakage_rate_unique']}
providers=[]
for stem,terms in names.items():
 p=R/'kernel/TGLExt'/f'{stem}.lean'; s=p.read_text(encoding='utf8')
 for term in terms:
  m=re.search(r'^(?:def|theorem) '+term+r'\b',s,re.M); assert m,term
  end=s.find(':=',m.start()); assert end!=-1
  providers.append(dict(name='TGLExt.'+term,path=str(p),canonical_path=str(Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')/p.name),line=s[:m.start()].count('\n')+1,sha256=sha(p),exact_statement=s[m.start():end].strip(),type_match='EXATO após especializar beta=c.beta; reflexão termina em sqrt(beta)^2 e exige Real.sq_sqrt; custo exige normalização alpha=beta/exp(1/2).',decision='REUSAR/ADAPTAR, sem reprovar fornecedor'))
u=R/'um.py'; lines=u.read_text(encoding='utf8').splitlines()
need=['"ext_rp_hubble_form_kernel_proved":','"ext_vc_pruning_is_reflection_kernel_proved":','"ext_fh_boundary_radical_kernel_proved":','"ext_nfw_rate_unique_kernel_proved":','def prove_d1_camb_protocol','"hypothesis": {"background":']
consumers=[dict(path=str(u),canonical_path=r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py',line=i+1,text=s.strip(),sha256=sha(u)) for i,s in enumerate(lines) if any(n in s for n in need)]
target='''structure TGLExt.TGLCoupling: beta : Real; beta_pos : 0 < beta; beta_lt_one : beta < 1.
def TGLCoupling.alpha c := c.beta / Real.exp (1/2).
the_same_beta_reads_three_faces (c : TGLCoupling) (rho_r rho_m rho_Lambda : Real):
 normSq(Smat(thetaMiguel c.beta).mulVec e1 1)=c.beta AND
 (0<c.alpha AND c.alpha<1 AND c.beta=c.alpha*exp(1/2) AND c.beta=c.alpha*sqrt(exp 1)) AND
 closure_identity(c.beta,rho_r,rho_m,rho_Lambda) AND hubble_form(c.beta,rho_r,rho_m,rho_Lambda) AND
 (forall t gap, 0<t -> 0<gap -> exp(-(t*c.beta*gap))<1) AND
 (forall b, (forall t, exp(-(t*b))=exp(-(t*c.beta))) -> b=c.beta).
The references to closure_identity and hubble_form above abbreviate their full equality propositions, recorded verbatim in providers, not proof objects used as propositions.'''
record=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO',order='ORDEM_012 B1',previous_goal_turn='PROGRESSO: potencias imaginarias aceitas; escala e antiunitario pendentes ficam congelados por precedencia expressa da ORDEM012.',
 exact_target=target,decision='ADAPTAR: instanciar os fornecedores na projeção única c.beta; NOVO apenas termo de dados com alpha definida, ponte sqrt(beta)^2=beta, identidade do custo e conjunção consumível. Não duplicar CFC, ângulo, fundo nem vazamento.',
 consumers=consumers,proposed_consumer=dict(map_entry='ext_same_beta_reads_three_faces_kernel_proved',declaration='TGLExt.the_same_beta_reads_three_faces',existing_anchor='ext_rp_hubble_form_kernel_proved / ext_vc_pruning_is_reflection_kernel_proved',protocol='prove_d1_camb_protocol: hypothesis.background e hypothesis.beta_theory',implementation_owner='gerência; nenhum mapa Python alterado aqui',B1_does_not_prove='H^2=...; B2-B4 ligam a identidade algébrica à equação métrica. B1 não altera D1.'),
 providers=providers,searches=json.loads((R/'BUSCAS_B1.json').read_text(encoding='utf8')),
 limitations=['Definir alpha pelo custo é normalização de forma, não derivação do valor CODATA.', 'Sem numeral atribuído a beta ou alpha; 0 e 1 são limites do domínio.', 'Sem hipótese sin²θ=beta adicionada: é conclusão do fornecedor aplicado.', 'Nenhum gate modificado.', '941 entradas distintas lidas no dicionário embutido; ordem declara942. Números não equiparados silenciosamente.', 'Pesquisa do acervo tem corte --max35; não demonstra exaustão das ocorrências. Busca canônica por tipo e nome é a prova de reaproveitamento local.'],
 validation_plan=['lake build TGLExt.TheSameBetaReadsThreeFaces em cópia isolada v353 sem objetos TGL/TGLExt herdados','lake build TGLExt.AuditSameBeta com nomes completos e axiomas no trio','controles negativos: substituir beta por alpha na reflexão e retirar o custo exp(1/2)','leitura/recompilação independente; entrega no túnel sem incorporação canônica'])
put(R/'REAPROVEITAMENTO_B1.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
md='''[OPEN — ficha de aproveitamento escrita antes do código B1]

# B1 — o mesmo beta nas faces de ângulo, custo e fundo

O único dado escalar é beta em (0,1). Alpha é definida como beta/exp(1/2), sem escolha de valor. A relação do custo é uma identidade desta normalização, não a dedução de CODATA. O teorema de reflexão existente será especializado e sqrt(beta)^2 reduzido a beta. Os dois teoremas de fundo e as propriedades da taxa serão aplicados literalmente ao mesmo campo.

Consumidor proposto: `ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces` no mapa já existente. Âncoras atuais e linhas verificadas constam abaixo. A hipótese `background` do protocolo D1 é consumidor posterior via B2–B5: B1 paga a identidade do acoplamento, não a equação de Friedmann. A gerência fará a incorporação.

Decisão: ADAPTAR fornecedores; NOVO apenas o termo compartilhado e as pontes necessárias. Não há reconstrução dos fornecedores. Nenhum valor numérico beta/alpha, inferência física ou mudança de gate.

## Tipo exigido
```text
'''+target+'\n```\n\n## Consumidores verificados\n'
for c in consumers: md+=f"- {c['canonical_path']}:{c['line']} — `{c['text']}`\n"
md+='\n## Fornecedores lidos\n'
for p in providers: md+=f"\n### {p['name']}\n{p['canonical_path']}:{p['line']} · SHA256 `{p['sha256']}`\n\n```lean\n{p['exact_statement']}\n```\n\n{p['type_match']} Decisão: {p['decision']}.\n"
md+='\n## Buscas e limites\n'+json.dumps(record['searches'],ensure_ascii=False,indent=2)+'\n\n'+'\n'.join('- '+s for s in record['limitations'])+'\n\n'+record['timestamp']+'\n'
put(R/'REAPROVEITAMENTO_B1.md',md.encode('utf8'))
print(json.dumps(dict(providers=len(providers),consumers=len(consumers),ficha_sha256=sha(R/'REAPROVEITAMENTO_B1.json'))))
