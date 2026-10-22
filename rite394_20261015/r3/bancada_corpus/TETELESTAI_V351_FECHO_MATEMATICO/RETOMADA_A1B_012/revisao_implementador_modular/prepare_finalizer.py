from pathlib import Path
import ast, json

OUT=Path(__file__).resolve().parent
R=OUT.parent
src=R/'revisao_vetores_fixos_modulares/finish_review.py'
s=src.read_text(encoding='utf8')
paragraphs=[
 '[REAL — tipos] Um teorema público, zero privados e zero definições. scalarTomitaImaginaryPower_eq_regular_implementation recebe somente P:SiteProfile, t:ℝ e x:ScalarGNSHilbert P. Conclui a igualdade do U original com π(λ_t) regularRightGNS(-t), em TODO vetor. Não recebe igualdade de grupos, totalidade, vetor cíclico, tracialidade ou identidade de produtos ilimitados como hipótese. As estruturas anteriores do mesmo P permanecem as mesmas.',
 '[REAL — família fixa] d_n=1/(n+1)>0 e e_n=regularAverage(P,d_n). choose Z hZ hU aplica o fornecedor regularAverage_square_modular_fixed a n apenas: Z_n e sua igualdade ambiente exata e_n*e_n são escolhidos antes da especialização hU n t; uma única família serve a todos os tempos. Z_n é auto-adjunto e pertence a scalarPolarRightAlgebra por star/mul dos elementos e_n já pagos. Não declara e_n auto-adjunto.',
 '[REAL — sinal e W] StrongIntegral.operatorIntegral_commutes e a lei abeliana de λ provam comutação de λ_s com eδ. Estrelar a igualdade em -t dá comutação com eδ*, daí com Z_n. W é apenas let local do operador limitado π(λ_t)R_-t. As identidades direita/esquerda originais dão WΛZ_n=Λ(λ_t Z_n λ_-t)=ΛZ_n. O sinal negativo vem da inversa efetiva λ_-t=λ_t*, não de troca de J linear por antilinear.',
 '[REAL — concordância] A covariância all-core anterior e hU n t calculam U_tπ(a)ΛZ_n. Para W, regularRightGNS_commutes_left vale para TODO a do core, e a unitariedade de πλ_t junto de WΛZ_n=ΛZ_n fornece a mesma expressão π(λ_t a λ_t*)ΛZ_n. Não se infere unicidade do implementador apenas de covariância; a concordância é demonstrada nesta família específica.',
 '[REAL — totalidade demonstrada] A cota ||Z_n||≤1 vem das contrações e_n. bounded_application_tendsto usa simultaneamente e_n v→v e e_n* v→v, para obter Z_n v→v; não assume continuidade forte geral da estrela. A continuidade forte limitada da MESMA π transporta Z_n→I ao H_I. Conjugação pelo J original contínuo, com Z_n*=Z_n, dá ρ(Z_n)→I fortemente. Para cada a∈nν, a identidade direita de E e o entrelaçamento esquerdo produzem π(a)ΛZ_n=ρ(Z_n)Λa→Λa. A densidade do Λ original e continuidade dos dois operadores completam a igualdade em TODO H_I. Não se pressupõe que qualquer ΛZ_n isolado seja cíclico.',
 '[REAL — fornecedores e ficha] Doze entradas da ficha e a assinatura integral corrigida do adendo foram confrontadas por linhas/bytes com fontes e cópias V. A ficha histórica truncou operatorIntegral_commutes dentro de (H := H); o adendo posterior ao DEV e anterior ao aceite registra o tipo completo. A anterioridade da leitura integral é declarada pelo autor; nesta revisão a leitura integral foi refeita diretamente e o tipo compila. A correção documental não cria uma hipótese ou novo fornecedor matemático. O replay antigo V350ScalarRegularPolarCommutation foi necessário também no V: um módulo com quatro declarações antigas, contado separadamente do novo alvo.',
 '[REAL — história e controle] Quatro DEV preservados: três rc1 excluídos (objeto antigo ausente, erros de composição/coerção, timeout de reescritas) e o final011125 rc0 sem avisos. maxHeartbeats2200000 e synthInstance200000 permanecem; o stdout DEV final vazio não foi tratado como auditoria de axiomas. Os auditores completos próprio/autoral fornecem o trio. BadModularImplementationRightSignChanged troca R_-t por R_t: as execuções própria e autoral recusam a aplicação por Type mismatch com imports válidos. Isso não é prova de impossibilidade por qualquer outro argumento.',
 '[REAL — independência e limites] Somente fontes do alvo e do fornecedor antigo ausente foram copiadas; o Lake próprio usa objetos anteriores produzidos no V e caches de pacotes pinados. Nenhum objeto K/DEV foi herdado. A ressalva histórica de autoria dos dois módulos antiunitários continua a dos40, inspecionados pelo principal; não é reclassificada aqui. Esta igualdade de implementadores está paga no escopo formal. Q, compatibilidade de meias potências/domínios, tracialidade do scalarInverseLimitWeight e contrato de traço continuam OPEN; nenhum gate, memória, monólito ou recibo foi alterado.'
]
start=s.index('PARAGRAPHS='); end=s.index('\ndef main():',start)
s=s[:start]+'PARAGRAPHS='+repr(paragraphs)+'\n'+s[end:]
def rep(a,b,n=None):
 global s
 k=s.count(a)
 assert k==(n if n is not None else 1),(a,k)
 s=s.replace(a,b)
rep('assert len(names)==2 and len(re.findall', 'assert len(names)==1 and len(re.findall')
rep("r'^theorem\\s+',code,re.M))==2", "r'^theorem\\s+',code,re.M))==1")
rep("r'^private theorem\\s+',code,re.M))==1", "r'^private theorem\\s+',code,re.M))==0")
rep('AUDITORIA_VETORES_FIXOS_MODULARES_A1B','AUDITORIA_IMPLEMENTADOR_MODULAR_A1B')
rep("==(2,0,1)","==(1,0,0)")
rep("author['modular_fixed_vectors_constructed']","author['implementator_equality_proved']")
rep('dev_modular_fixed_vectors','dev_modular_implementation')
rep('V351ModularFixedVectors.lean','V351ModularImplementation.lean')
rep("jd.get('providers',[])+jd.get('extra_providers',[])","jd.get('providers',[])+([jd['corrected_provider']] if 'corrected_provider' in jd else [])")
rep('assert len(checks)==10','assert len(checks)==13')
rep('REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES','REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR')
rep("consumer_status='IMPLEMENTATOR_EQUALITY_STILL_OPEN'","consumer_status='IMPLEMENTATOR_EQUALITY_PROVED__QUADRATIC_TRACE_OPEN'")
rep("assert not [x for x in s['sources'] if not x['target'] and not x['source_preexisting']]", """oldnew=[x for x in s['sources'] if not x['target'] and not x['source_preexisting']]
 assert {x['module'] for x in oldnew}=={'TGLExt.V350ScalarRegularPolarCommutation'}
 old_audits=[]
 for x in oldnew:
  tr,tj,mi=trace(x['module']);oa=parse_axioms('\\n'.join(mi))
  assert len(oa)==4 and all(set(v)<=ALLOWED for v in oa.values())
  old_audits.append(dict(module=x['module'],source=x,trace=pin(tr),axioms=oa,new_theorems_counted=False))
 pr=load(R/'ADENDO_FICHA_IMPLEMENTADOR_MODULAR.json')['provider_replay']
 ck(pr);pj=load(Path(pr['path']));validate_pin_tree(pj,[])
 assert pj['returncode']==0 and pj['source_bytes_unchanged'] and len(pj['new_or_changed_objects'])==1
 save(OUT/'old_supplier_replay_read.json',dict(author=pr,author_metadata=pj,own=old_audits))
 expected_new=set(s['modules']+[s['auditor_module']]+[x['module'] for x in oldnew])""")
rep("==set(s['modules']+[s['auditor_module']])","==expected_new",2)
rep('exact_target_count=2,new_theorems=2,new_definitions=0,private_theorems=1,private_definitions=0','exact_target_count=1,new_theorems=1,new_definitions=0,private_theorems=0,private_definitions=0',2)
rep('total_source_theorems_including_private=3','total_source_theorems_including_private=1')
rep('newly_recompiled_old_supplier_count=0,newly_recompiled_old_suppliers=[]','newly_recompiled_old_supplier_count=len(oldnew),newly_recompiled_old_suppliers=old_audits,old_supplier_replay=pin(OUT/\'old_supplier_replay_read.json\')')
rep('implementator_equality_proved=False','implementator_equality_proved=True',2)
start=s.index(' limits=[');end=s.index('\n report=dict',start)
s=s[:start]+""" limits=['Aceite32: um teorema público, zero privados/defs; um fornecedor antigo de quatro declarações reconstruído separadamente, além do auditor próprio.', 'U_t=π(λ_t)R_-t em TODO H_I original está demonstrado. Q, meias potências/domínios, tracialidade e contrato de traço continuam abertos; não há h=Delta_nu.', '19 V351 são subconjunto das 940 entradas da base, não959. Preservação relida em bytes.', 'Somente esta pasta e novas saídas em V foram escritas; K/OLD/V353, memórias, monólito, writers e predecessores preservados.']"""+s[end:]
rep('dois tipos completos com universos','um tipo completo com universos')
rep("' novos (alvo+auditor), total '","' novos (alvo+auditor+um fornecedor antigo), total '")
rep("'. Nenhum fornecedor antigo recompilado, nenhum objeto K/DEV herdado.","'. Um fornecedor antigo reconstruído de fonte, nenhum objeto K/DEV herdado.")
rep("' mensagens de fornecedores herdadas discriminadas.","' mensagens de fornecedores discriminadas em supplierwarnings (old_object indica herança).")
# Record the fixed heartbeat budget and actual source snapshot for every historical run.
rep("ck(j['stdout']);ck(j['stderr'])", """ck(j['stdout']);ck(j['stderr'])
  hist_code=uncomment((q.parent/'V351ModularImplementation.lean').read_text(encoding='utf8'))
  assert re.findall(r'set_option maxHeartbeats (\\d+)',hist_code)==['2200000']
  assert re.findall(r'set_option synthInstance.maxHeartbeats (\\d+)',hist_code)==['200000']""")
rep("full_trace_constructed=False)","full_trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False)")
rep("trace_constructed=False,gate_modified=False)","trace_constructed=False,quadratic_trace_compatibility_proved=False,gate_modified=False)")
ast.parse(s)
p=OUT/'finish_review.py';assert not p.exists()
t=p.with_name(p.name+'.tmp');t.write_bytes(s.encode('utf8'));assert t.read_bytes()==s.encode('utf8');t.replace(p)
print('FINALIZER_PREPARED',p)
