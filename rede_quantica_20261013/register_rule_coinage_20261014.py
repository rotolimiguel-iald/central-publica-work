"""Custody of the operator's coinage; no theorem or external dispatch."""
import datetime as dt
import json
import subprocess
from pathlib import Path
from diary_r1 import ROOT,WORK,PY,WHO,CLI,new,pin,append_bytes

U='F1.REGRA'
D=ROOT/'work/cunhagem_regra_20261014'
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/U
TEXT='Agora eu consigo cunhar a última pedra que falta, que é a definição de regra. O que é regra? Regra é igual a direito, e isso parece uma contradição, porque direito parece ser uma aquisição. Não é, é uma negação. Regra é negar tudo aquilo que não pode ser, e isso é criar limite assintótico. Portanto, direito não é uma aquisição no sentido de uma autoafirmação como condição de suporte, mas é uma aquisição no sentido de haver um espaço possível de inscrição, de possibilidade, e isso só se dá pela delimitação, que é negativa, não positiva. Portanto o direito é negativo e não positivo. Cria-se aqui o domínio da negatividade jurídica.'

def call(args,payload=None,receipt=None):
 cp=subprocess.run([PY,'-B','-X','utf8',*map(str,args)],input=None if payload is None else json.dumps(payload,ensure_ascii=False),capture_output=True,text=True,encoding='utf-8')
 try:value=json.loads(cp.stdout)
 except json.JSONDecodeError:value=None
 if receipt:new(OUT/receipt,{'command':[str(x) for x in args],'exit_code':cp.returncode,'result':value,'text':cp.stdout if value is None else None,'stderr':cp.stderr})
 if cp.returncode:raise RuntimeError(cp.stderr or cp.stdout)
 return value

def source(p):
 q=pin(p);return {'kind':'artifact','ref':q['path'],'sha256':q['sha256']}

def main():
 D.mkdir(exist_ok=True)
 prior=call([CLI,'ver','F1.REDE'])
 definition=D/'CADASTRO_UNIDADE.json'
 # The minimal input is required by the board API to create a unit; no concept or memory is written before claim.
 if not (OUT/'QUADRO_INICIAL.json').exists():
  new(definition,[{'id':U,'frente':prior['frente'],'titulo':'Custódia da cunhagem de regra e negatividade jurídica','status':'PROPOSTA','dono':WHO,'criterio':'Verbatim integral com hash; leitura do Atlas; comentário ao lado com estatutos; memória aditiva com backups. Não inclui construção Lean, parecer jurídico ou pesquisa nova.','fonte':'Mensagem humana direta de14/10/2026 nesta conversa','dependencias':[]}])
  created=call([CLI,'nova','--json',definition,'--quem',WHO])
  claimed=call([CLI,'reivindicar',U,'--quem',WHO,'--nota','Custodiar cunhagem humana integral e comentário tipado. Superficies: memory/DIARIO_CONSTRUCAO_QG.md, memory/TGL_ATLAS.md, memory/TGL_INDICE_VIVO.md, ORDEM_019/AVISO_GERENCIA.md e ACOM propria. Sem envio, kernel ou parecer juridico.'])
  OUT.mkdir(exist_ok=True)
  new(OUT/'QUADRO_INICIAL.json',{'creation':created,'claim':claimed,'bootstrap':pin(definition)})
 else:
  initial=json.loads((OUT/'QUADRO_INICIAL.json').read_text(encoding='utf-8'));claimed=initial['claim']
  current=call([CLI,'ver',U])['reivindicacao'];assert current['quem']==WHO
  assert dt.datetime.fromisoformat(current['vence_em'])>dt.datetime.now(dt.timezone.utc)
 if not (OUT/'CONSULTA_NOS_VIVO.json').exists():
  call([r'C:\IALD\NOS_VIVO\consultar.py','--unidade',U],receipt='CONSULTA_NOS_VIVO.json')
 lookup=json.loads((OUT/'CONSULTA_NOS_VIVO.json').read_text(encoding='utf-8'))
 if lookup['exit_code']:
  assert 'unidade não está no grafo' in (lookup['stderr'] or lookup['text'] or '')
  new(OUT/'LIMITACAO_GRAFO.json',{'status':'NEW_UNIT_NOT_YET_INDEXED','failed_lookup':pin(OUT/'CONSULTA_NOS_VIVO.json'),'action':'Original failure retained. Direct Atlas consultation and route search provide the documentary reuse; no kernel construction or graph rebuild.'})
 call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','negatividade|regra|admissibilidade'],receipt='CONSULTA_MAPA.json')
 original=OUT/'OPERADOR_REGRA_NEGATIVIDADE_VERBATIM_20261014.txt';new(original,TEXT)
 atlas=ROOT/'memory/TGL_ATLAS.md';lines=atlas.read_text(encoding='utf-8').splitlines()
 excerpts=[{'first_line':20177,'last_line':20182,'text':'\n'.join(lines[20176:20182])},{'first_line':20513,'last_line':20530,'text':'\n'.join(lines[20512:20530])}]
 new(OUT/'REAPROVEITAMENTO_ATLAS.json',{'source':pin(atlas),'excerpts':excerpts,'scope':'Custódia, nome cunhado como obrigação de prova e analogia estrutural jurídica já constam. A nova formulação é acrescentada com autoria; busca literal não localizou negatividade jurídica nas superfícies consultadas, sem alegar inédita em todo acervo/literatura.'})
 commentary='''[ONTO — cunhagem do operador] Regra = direito; direito constituído pela exclusão do que não pode ser, delimitando possibilidade de inscrição. O verbatim permanece integral acima. A expressão «última pedra» é a avaliação do autor nesta mensagem; não é um atestado de completude matemática produzido pelo registro.

[PARÁFRASE DO ASSISTENTE] A delimitação negativa constitui o espaço admissível em que uma inscrição pode ocorrer. «Negativo» designa aqui o modo de constituição; seu alcance não é identificado automaticamente com terminologia jurídica técnica preexistente.

[DERIVED — representação proposta, não teorema Lean] Dados um universo X e um predicado nomeado I_R(x) de inadmissibilidade, representar D_R = {x em X | não I_R(x)}. Essa escrita explicita exclusão/admissibilidade. Por si só, não demonstra a primazia ontológica da negação nem produz norma a partir de um fato físico. O critério I_R precisa ter domínio e fundamento declarados; impossibilidade lógica, incompatibilidade física e inadmissibilidade normativa não são intercambiáveis por homonímia.

[OPEN — obrigações do contrato] (1) Exibir x em D_R se se pretende um espaço efetivamente possível: excluir tudo deixa D_R vazio. (2) Especificar topologia/métrica e dinâmica para falar em limite assintótico. A definição de D_R por exclusão não fornece convergência; por exemplo, excluir nada admite uma órbita periódica. Uma possível condição futura é dist(T_t(x),D_R) tender a zero; ela tampouco afirma por si só um ponto limite único. (3) Se houver operador de leitura/projeção, construir sua relação com D_R e provar suas propriedades, sem recebê-las como nomes vazios.

[REAL — reaproveitamento documental] Atlas XI.B/J.7 já qualifica o acoplamento jurídico como analogia estrutural [ONTO] e distingue interpretação de derivação; XI.B/J.1 registra custódia por negação e nome cunhado como obrigação de prova. A nova cunhagem conversa com essas entradas, preservadas integralmente. Nenhuma prova anterior é reclassificada, nenhum gate muda e nenhum acervo do Escritório foi consultado.'''
 note=OUT/'CUNHAGEM_E_ALCANCE_20261014.md'
 new(note,'# Regra e domínio da negatividade jurídica\n\nAutor da cunhagem: Luiz Antonio Rotoli Miguel. Data da mensagem:14/10/2026. Unidade:'+U+'.\n\n## Verbatim integral\n\n'+TEXT+'\n\n## Ao lado — estatutos e proposta de representação\n\n'+commentary+'\n\nSHA256 do verbatim: `'+pin(original)['sha256']+'`.\n')
 marker='coinage_rule_negative_20261014'
 section='\n\n## 14/10/2026 — Regra e domínio da negatividade jurídica\n<!-- '+marker+' -->\n\nEm nome de '+WHO+', sob reivindicação '+str(claimed.get('evento'))+'. [ONTO — cunhagem de Luiz Antonio Rotoli Miguel; mensagem humana direta]\n\n'+TEXT+'\n\nAo lado: [DERIVED — proposta] D_R={x em X | não I_R(x)}. [OPEN] Critério tipado de inadmissibilidade, não vacuidade e dinâmica/convergência necessária ao caráter assintótico. A definição por exclusão não prova, sozinha, limite assintótico ou completude da QG.\n\nOriginal: `'+str(original)+'`; SHA256 `'+pin(original)['sha256']+'`. Comentário separado: `'+str(note)+'`. Reaproveitado Atlas XI.B/J.1 e J.7, preservando analogia [ONTO] e obrigação de prova.\n'
 receipts=[]
 for p in [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',atlas,ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
  receipts.append(append_bytes(p,section,marker))
 new(OUT/'MEMORY_RECEIPT.json',{'unit':U,'claim':claimed,'surfaces':receipts,'original':pin(original),'commentary':pin(note)})
 result=OUT/'RESULTADO_CUSTODIA.json';new(result,{'unit':U,'status':'CUSTODY_COMPLETED_SCIENTIFIC_CONSTRUCTION_NOT_CLAIMED','original':pin(original),'commentary':pin(note),'reuse':pin(OUT/'REAPROVEITAMENTO_ATLAS.json'),'memory':pin(OUT/'MEMORY_RECEIPT.json')})
 entry=OUT/'MAP_ENTRY.json';new(entry,{'tipo':'ROTA','rota_id':'conceitual.regra.negatividade_juridica','dominio':'JURIDICO_ONTOLOGICO','titulo':'Regra e domínio da negatividade jurídica — cunhagem do operador','pergunta':'Como a exclusão do inadmissível delimita o espaço possível de inscrição?','dados':['Mensagem humana direta de14/10/2026','Atlas XI.B/J.1 e J.7'],'metodo':'Custódia literal, hash de bytes e comentário ao lado com estatutos.','resultado':'Verbatim preservado. Representação candidata D_R={x|não I_R(x)}; não vacuidade e caráter assintótico permanecem obrigações explícitas.','veredito':'CUNHAGEM_CUSTODIADA__FORMALIZACAO_PROPOSTA','estatuto':'ONTO','status':'EXAMINADA','olhou_dados':False,'defeito':'A exclusão não demonstra sozinha convergência assintótica, domínio não vazio ou primazia ontológica.','nao_refazer':'Reaproveitar a custódia integral e as entradas J.1/J.7; não encadear os regimes por homonímia.','proximo_passo':'Discussão com o autor sobre o contrato; nenhuma construção Lean iniciada nesta unidade de custódia.','onde':str(OUT),'artefatos':[str(original),str(note),str(result)],'refs':[],'nota':'Memória aditiva sob unidade própria; nenhum provedor, kernel, dado observado ou gate.'})
 call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO+' / '+U],receipt='MAP_RECEIPT.json')
 call([CLI,'avancar',U,'--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Custodia literal da cunhagem de14out; comentario ao lado ONTO/DERIVED/OPEN e memoria com backups. Nao se reivindica prova Lean ou fechamento QG.'],receipt='BOARD_DELIVERY.json')
 call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':8,'event_id':'rule-negative-coinage-20261014','actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'rule-negative-coinage-20261014','kind':'fact','statute':'ONTO','text':'Cunhagem direta do operador: Regra = direito; delimitação negativa constitui espaço possível de inscrição; domínio da negatividade jurídica. Original integral custodiado em F1.REGRA. Comentário ao lado propõe D_R={x|não I_R(x)}, preservando não vacuidade e caráter assintótico como obrigações. Nenhuma completude matemática inferida.','sources':[source(original),source(note),source(result)]}]}},receipt='ACOM_RECEIPT.json')
 call([CLI,'liberar',U,'--quem',WHO,'--nota','Custodia e memoria entregues; formalizacao permanece proposta tipada.'],receipt='RELEASE.json')
 print(json.dumps({'unit':U,'original':pin(original),'note':str(note),'result':str(result),'claim_event':claimed.get('evento')},ensure_ascii=False))

if __name__=='__main__':main()
