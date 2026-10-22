"""Append claimed memory with byte backups and create new delivery manifests."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019');B=R/'F0.3.B2';N=R/'F8.2.NU4'
def read(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,x):
 with p.open('x',encoding='utf-8') as f:json.dump(x,f,ensure_ascii=False,indent=2,allow_nan=False)
bs=B/'RESULTADO_IMPLANTACAO_20261010_R1.json';ns=N/'RESULTADO_ENTREGA_R1.json';mr=B/'MEMORY_RECEIPT_DEPLOY_NU4_20261010_R1.json'
for p in (bs,ns,mr):
 if p.exists():raise FileExistsError(p)
br=sorted((B/'review').glob('*20261010_R1*'));nr=sorted((N/'review').glob('*'))
for files in (br,nr):
 assert any(p.suffix=='.json' for p in files) and any(p.suffix=='.md' for p in files),'review missing'
r=read(N/'RESULTADOS_R1.json');l=read(B/'LIVE_VERIFICATION_R1.json');s=read(B/'RESTART_RECEIPT_R1.json')
assert l['ok'] and r['verdict']=='INSTALLED_BENCH_CONDITIONAL_PILOT_PASS'
assert (N/'review'/'PARECER_R2.md').exists(), 'Final reviewer R2 required'
now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%d_%H%M%S')
refs=[pin(B/'RELATORIO_IMPLANTACAO_20261010_R1.md'),pin(B/'LIVE_VERIFICATION_R1.json'),pin(N/'PRIMEIROS_RESULTADOS_R1.md'),pin(N/'RESULTADOS_R1.json')]
text='\n\n### 10/10/2026 — Bancada instalada e primeiro ensaio de neutrinos [codex-gerente-tgl]\n<!-- F03B2_DEPLOY_F82NU4_20261010_codex -->\n\n'
text+='[INPUT] Resposta do operador após pedido específico de implantação: «continue até rodar o teste e termos os primeiros resultados». Retomada F0.3.B2 reivindicação639, com estas três superfícies nomeadas; ensaio F8.2.NU4 reivindicação642. Reaproveitamento NU2/NU3/F7.2 e consultas ao Nós Vivo/mapa preservados. A unidade nova ainda não consta do grafo.\n\n'
text+=f"[REAL — estado posterior, em nome de codex-gerente-tgl] A pendência de implantação do adendo anterior foi resolvida após a resposta do operador e a autorização da revisão automática. Instalação com backups e reinício; HTTP e MCP novo conferidos (28 ferramentas). Processo atual registrado: {s['new_server']}; clientes MCP anteriores precisam reconectar, sem verificação de todas as sessões. Manifesto {r['canonical']['canonical_manifest_sha256']}; programa {r['canonical']['canonical_version']} ({r['canonical']['um_py_sha256']}); selo {r['canonical']['seal_sha256']}. A guarda confere identidade por operação e recusa divergência; versão nova requer implantação testada. Recibos antigos permanecem intactos; LIVE_VERIFICATION_R1 resolve a etapa operacional.\n\n"
text+=f"[REAL computacional; DERIVED condicional] O protocolo pinado antecedeu16 chamadas ao serviço instalado:52,5km,2/4/8MeV,tau_star=tP,Kfac=1,beta0=alpha*sqrt(e) em runtime. DeltaPee={[x['delta_Pee_stable'] for x in r['reactor']]}. Taxas E^-2; traço/positividade aprovados; energia Tr(rho H) do gerador diagonal fixo conservada. Estado diagonal permaneceu igual nas três amplitudes. Controle positivo detectou DeltaPee={r['positive_control']['delta_Pee']}, com amplitude instrumental declarada. A expressão estável conserva o efeito que a subtração double arredonda a zero. tau=tP é instância condicional, não determinação física.\n\n"
text+='[ALCANCE] Contratos existem nos artigos e foram recuperados. O ensaio não produziu sigma observado, luminosidade ou Massa de Chandrasekhar, nem exclui todos os canais da TGL. A composição produção/transporte/Ye/estrutura estelar e as amplitudes pertinentes continuam por explicitar. Conferência independente local documentada em review, sem equivalência com auditoria c1. Sem fit observado, rito selado aberto, comunicação Claude/provedor ou alteração de um.py/kernel/gate. Sem nova versão selada ou mudança do caminho formal: nenhuma escrita na linhagem do Nós.\n\n'
text+='Referências (hashes lidos dos bytes):\n'+'\n'.join('- '+v['path']+' — '+v['sha256'] for v in refs)+'\n'
receipts=[]
for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','TGL_CORE_MEMORY.md']:
 p=Path(r'C:\IALD\Central de Patentes\memory')/name;b=p.read_bytes();out=b+text.encode('utf-8')
 assert b'F03B2_DEPLOY_F82NU4_20261010_codex' not in b
 bak=p.with_name(p.name+'.bak_'+stamp);tmp=p.with_name(p.name+'.tmp_'+stamp)
 with bak.open('xb') as f:f.write(b)
 assert bak.read_bytes()==b
 with tmp.open('xb') as f:f.write(out);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==out and len(out)>len(b)
 os.replace(tmp,p);assert p.read_bytes()==out
 receipts.append(dict(before_sha256=hashlib.sha256(b).hexdigest(),backup=pin(bak),after=pin(p),added_bytes=len(out)-len(b),prefix_preserved=True))
save(mr,dict(unit='F0.3.B2',claim=639,author='codex-gerente-tgl',at_utc=now.isoformat(),surfaces=receipts))
bf=['OPERADOR_CONTINUAR_20261010.txt','PREFLIGHT_20261010_R1.json','DEPLOY_PLAN_R1.json','DEPLOY_RECEIPT_R1.json','RESTART_BEFORE_R1.json','RESTART_RECEIPT_R1.json','LIVE_VERIFICATION_R1.json','RELATORIO_IMPLANTACAO_20261010_R1.md','MEMORY_RECEIPT_DEPLOY_NU4_20261010_R1.json','candidate/canonical_contracts.json']
nf=['PREREGISTRO_R1.json','run_pilot_r1.py','RESULTADOS_R1.json','PRIMEIROS_RESULTADOS_R1.md']+[c['path'] for c in r['calls']]
save(bs,dict(unit='F0.3.B2',claim=639,status='ENTREGUE',verdict='INSTALLED_AND_RUNTIME_VERIFIED',canonical=r['canonical'],runtime_verified=True,mcp_new_connection_verified=True,previous_clients_reconnection='NOT_ALL_VERIFIED',artifacts=[pin(B/f) for f in bf]+[pin(p) for p in br if p.is_file()],pilot=pin(N/'RESULTADOS_R1.json'),gate_effect='NONE',independent_check='Local independent review; not c1 audit'))
save(ns,dict(unit='F8.2.NU4',claim=642,status='ENTREGUE',verdict=r['verdict'],canonical=r['canonical'],observed_fit=False,nature_sigma=None,gate_effect='NONE',artifacts=[pin(N/f) for f in nf]+[pin(p) for p in nr if p.is_file()],memory_receipt=pin(mr),independent_check='Local independent review; not c1 audit'))
for folder,route,title,res,report in [(B,'infra.bancada_um.adequacao_canonica_persistente','Bancada instalada, v391 e runtime conferidos',bs,B/'RELATORIO_IMPLANTACAO_20261010_R1.md'),(N,'sn.neutrinos.primeiro_ensaio_bancada_canonica','Primeiro ensaio condicional:16 chamadas e controles aprovados',ns,N/'PRIMEIROS_RESULTADOS_R1.md')]:
 save(folder/'MAPA_ENTREGA_20261010_R1.json',dict(tipo='RESULTADO',rota_id=route,dominio='INFRAESTRUTURA' if folder==B else 'SUPERNOVA_IA',titulo=title,status='EXAMINADA',estatuto='REAL computacional; DERIVED condicional',veredito='INSTALLED_AND_RUNTIME_VERIFIED' if folder==B else r['verdict'],olhou_dados=False,artefatos=[str(res),str(report),str(mr)],nota='Implantação após resposta do operador e revisão automática. Ensaio sintético/de referência; sem sigma observado ou gate movido. Revisões independentes locais documentadas; aguarda auditoria c1.'))
print(json.dumps(dict(memory=pin(mr),deployment=pin(bs),pilot=pin(ns)),ensure_ascii=False,indent=2))
