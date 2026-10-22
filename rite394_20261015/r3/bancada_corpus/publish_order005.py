"""Publish an immutable local reply to order 005, with measured hashes."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def publish(p,text):
    assert not p.exists(),str(p)
    b=text.encode('utf-8')
    t=p.with_suffix(p.suffix+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.stat().st_size==len(b)
    t.rename(p)
tests=load('JOINT_CONTOUR_V1_CONTROLES.json')
mass=load('ORDEM005_MASSA_CONTROLES.json')
eligibility=load('JOINT_CONTOUR_V1_ELEGIBILIDADE.json')
assert len(tests['tests'])==13 and len(mass['rows'])==6
assert eligibility['real_joint_statistic_computed'] is False
source=ROOT/'Order005Algebra.lean'
names=re.findall(r'^theorem\s+(\w+)',source.read_text(encoding='utf-8'),re.M)
meta_path=sorted(ROOT.glob('Order005Algebra.*.json'))[-1]
meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
assert meta['exit_code']==0 and meta['source_stable'] is True and meta['proof_sha256']==sha(source)
log=ROOT/meta['log']
content=log.read_text(encoding='utf-8-sig')
assert not re.search(r'\b(error|warning|sorryAx)\b',content)
printed=re.findall(r"'ChatgptAudit\.(\w+)' depends on axioms: \[([^\]]+)\]",content)
assert sorted(n for n,_ in printed)==sorted(names)
assert all(set(a.split(', '))=={'propext','Classical.choice','Quot.sound'} for _,a in printed)
verification={'theorem_count':len(names),'axioms':dict(printed),'lean_metadata':str(meta_path),
              'lean_metadata_sha256':sha(meta_path),'lean_log':str(log),'lean_log_sha256':sha(log),
              'engine_tests':len(tests['tests']),'rational_worlds':len(tests['exact_controls']),
              'historical_mass_rows':len(mass['rows']),'current_joint_status':eligibility['machine_result'],
              'sealed_result_and_source_verified':mass['provenance'],
              'independent_audit_pending':True}
publish(ROOT/'ORDEM005_VERIFICACAO_FINAL.json',json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
body='''[REAL] v98 reproduzida: seis âncoras, 13 controles de máquina e sete lemas Lean. [DERIVED condicional] forma de massa. [OPEN] realização física e combinação quantitativa dos quatro domínios.

# ENTREGA 005 — reabertura medida da v98 e JOINT_CONTOUR_V1

05/09/2026 · bancada ChatGPT → gerência Claude · resposta à ORDEM 005.

Parecer completo: ORDEM005_PARECER_FINAL.md. Derivações anteriores ao código: ORDEM005_DERIVACOES.md. Pré-registro proposto: JOINT_CONTOUR_V1_PREREG_DRAFT.md. Não houve alteração do programa vivo, do veto GA, de qualquer gate ou memória canônica.

## Resultado principal

M_GA=2,74354×10¹⁶ M☉ continua na janela. O defeito v98 era a extensão às âncoras galácticas: fatores 48,1323 e 144,3970, reproduzidos com os números históricos. O log contemporâneo confirma esse diagnóstico. A álgebra da forma condicional permanece; a ponte física de fonte e a admissibilidade não foram provadas por estes cálculos.

O rito conjunto de quatro domínios permanece JOINT_CONTOUR_INCONCLUSIVE. Os resumos disponíveis não fornecem quatro medições gaussianas independentes de β com covariância estabelecida. Nenhuma estatística conjunta real foi fabricada.

## Critérios, um a um

| Critério | Situação | Evidência e limite |
|---|---|---|
| A.1 Arqueologia exata | PAGO [REAL] | Log run_v98_stdout:626–635, §178, rito atual e resultado selado; seis contas reproduzidas. As fontes de literatura da tabela não foram reabertas; sem novas barras inventadas. |
| A.2 Rederivação e dimensões | PAGO como derivação CONDICIONAL; NÃO PAGO como lei física incondicional | Origem 2β²=β×β/(1/2), ponte de fonte, perfil radial e admissibilidade explícitos; unidades completas; R=57 tem origem atribuída e σ ausente. |
| A.3 Confronto | PAGO [REAL] | GA continua dentro, discrepâncias galácticas persistem; arredondar 40/0,7 afeta ~0,25%; identidade algébrica em Lean, números em dupla precisão. |
| A.4 Três saídas | PAGO | Reinstauração limpa ainda não justificada; extrapolação universal mantém defeito; enunciado condicional preservável. Errata proposta AO LADO, sem aplicação. |
| A.5 Decisão exclusiva | PAGO | Alcance do mandato/retirada e autorização editorial reservados ao operador. |
| B.1 Estatística e penalização | PAGO como contrato derivado; combinação real de quatro domínios NÃO DISPONÍVEL | Modelo gaussiano com C conhecida, constante fixa vs livre; ΔAIC=2−G. Vantagem máxima de A=2. Não é Bayes factor nem comparação com ΛCDM completo. |
| B.2 Correlações | PAGO como auditoria; matriz conjunta NÃO CONSTRUÍDA | JUNO/global, cosmologia/escala, réplicas VAST, GA/Coma inversa e circularidades antigas documentados. Sem presumir independência ausente. |
| B.3 Pré-registro | PAGO como RASCUNHO NÃO RATIFICADO | Hipóteses, roster, seleção, modelos de leitura, covariância, limiar bilateral, poder, hash, parada e veto. Adaptador canônico não aplicado; precisa de verificação real dos campos científicos e de autorização. |
| B.4 Controles exatos sintéticos | PAGO [REAL] | 13 casos de máquina; três mundos com quadráticas racionais; controles de χ²; sete lemas Lean condicionais/algébricos. |
| B.5 Decisão exclusiva | PAGO | Congelar ou não, com quais domínios e quais dados prospectivos, reservado ao operador. |

## Achados que a fiação precisa respeitar

O texto do rito neutrino exige duas determinações independentes ≥5σ; a implementação atual usa só a tensão global para emitir FALSIFIED. O rótulo indep=True em JUNO e global pós-JUNO não resolve a dependência. Corrigir/auditar isso antes de usar a saída como veto limpo.

O SNR=6,1867 do perfil de shear vem acompanhado de B-mode reprovado (χ²/dof=12,3714) e Fisher do piso zero. É registro de sinal bruto; não uma medição limpa de β. O piso de densidade e sua leitura qualitativa são objetos distintos. Coma está sem comparison revelada no resultado selado lido. GA está sem erros M,R e sem likelihood adequada; sua janela operacional ratificada é preservada.

## Reprodução

Em PowerShell, a partir de C:/IALD/Central de Patentes:

'''
q=chr(96)
body+=q*3+'''powershell
& 'C:/Python314/python.exe' -B './Chatgpt/audit_order005.py'
if ($LASTEXITCODE -ne 0) { throw 'Falha na auditoria 005' }
& './Chatgpt/verify_stage.ps1' -Module Order005Algebra
if ($LASTEXITCODE -ne 0) { throw 'Falha Lean 005' }
'''+q*3+'''

O script de auditoria importa apenas joint_contour_v1, construído nesta bancada; um.py é analisado por AST e JSONs são lidos. Não executa/importa o programa original ou seu snapshot. Saídas iguais são verificadas byte a byte; saídas diferentes são recusadas, jamais sobrescritas. Lean 4.31.0 lê dependências e escreve artefatos exclusivamente na bancada.

## Axiomas

Todos os sete lemas imprimiram exatamente [propext, Classical.choice, Quot.sound], sem novos axiomas, sorry ou avisos na compilação final. Eles provam identidades condicionais de massa/compactação e álgebra de comparação, NÃO a distribuição estatística, a ponte física ou as hipóteses científicas do teste. O log completo e os nomes estão na verificação final.

## Proveniência, falhas e limites

O hash do resultado lido coincide com seu selo, e uma cópia anterior do fonte coincide com o hash um.py desse selo. O snapshot corrente difere porque a casa evoluiu; as cinco funções auditadas têm AST idêntica entre fonte selado e corrente. Não se mistura a revisão corrente com uma falsa alegação de que ela já estava selada. As fontes e hashes estão nos registros.

A primeira execução do controle falhou porque o leitor numérico não aceitava uma fração representada como string; recusou com INCONCLUSIVE/INVALID_INPUT. Corrigido, com backups de bytes e registro ORDEM005_FALHA_001.md. O primeiro Lean compilou com um aviso de estilo; fonte e log preservados, aviso removido na compilação final. Houve também uma recusa inicial de leitura pelo sandbox; a leitura autorizada foi repetida com aprovação de acesso, sem escrita em originais.

Não foram abertos dados observacionais novos. A única pesquisa externa foi bibliográfica sobre o critério estatístico, com fonte primária citada nas derivações. Não há reinstauração, pré-registro ratificado, incorporação, confirmação ou mudança de gate nesta entrega. A próxima etapa científica exige preencher contratos de dados e validar a ponte de fonte; assinatura não substitui essas condições.

## Arquivos e SHA256 dos bytes

'''
files=['ORDEM005_PARECER_FINAL.md','ORDEM005_DERIVACOES.md','JOINT_CONTOUR_V1_PREREG_DRAFT.md',
       'joint_contour_v1.py','audit_order005.py','JOINT_CONTOUR_V1_SPEC_DRAFT.json',
       'JOINT_CONTOUR_V1_CONTROLES.json','JOINT_CONTOUR_V1_ELEGIBILIDADE.json','ORDEM005_MASSA_CONTROLES.json',
       'Order005Algebra.lean','ORDEM005_VERIFICACAO_FINAL.json','ORDEM005_FALHA_001.md',
       'ORDEM005_MEMORIA_EXCERTOS.json','ordem005_L4_theorem.md','ordem005_conversion_theorem.md',
       'ordem005_run_v98_stdout.txt','um_ordem005_snapshot.py','um_ordens003_004_snapshot.py',
       'ordem005_um_absoluto.json','ordem005_um_absoluto_selo.json','publish_order005.py',log.name,meta_path.name]
for name in files:
    p=ROOT/name
    body+=f'- {q}{p}{q} — {q}{sha(p)}{q}.\n'
body+='\nContagem lida do fonte Order005Algebra.lean: '+str(len(names))+' teoremas.\n'
body+='\nSomente o operador decide a revisão histórica da v98 e se autoriza congelar JOINT_CONTOUR_V1, com quais domínios e dados. A gerência audita antes de incorporar.\n'
target=ROOT/'TUNEL'/'DO_CHATGPT'/'ENTREGA_005_reabertura_v98_e_teste_conjunto.md'
publish(target,body)
print(json.dumps({'delivery':str(target),'sha256':sha(target),'theorems':len(names),'tests':len(tests['tests'])},ensure_ascii=False))
