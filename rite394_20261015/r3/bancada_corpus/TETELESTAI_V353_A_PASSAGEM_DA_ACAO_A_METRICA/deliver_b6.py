from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B6_importacoes_e_limites.md'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) or p==OUT
    assert not p.exists(),p
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
a=load(R/'AUDITORIA_B6.json');v=load(R/'revisao_b6/REVIEW_B6_FINAL.json');c=load(Path(v['compilation']['path']))
assert v['status']=='B6_DOCUMENTARY_REVIEW_ACCEPTED__PROPOSAL_NOT_INSTALLED' and all(not v[k] for k in ['P0','P1','P2'])
assert a['all_trio'] and a['new_theorems']==0 and c['all_accepted_builds_exit_zero']
assert c['all_axioms_allowed'] and not c['author_project_objects_copied'] and not c['new_B6_auditor_warnings']
assert c['exact_target_count']==len(a['targets'])==10 and load(Path(v['run']['path']))['returncode']==0
files=set()
def accept(x):
    if isinstance(x,dict):
        if {'path','bytes','sha256'}<=x.keys():
            p=Path(x['path']);assert pin(p)=={k:x[k] for k in ['path','bytes','sha256']},p;files.add(p)
        for y in x.values():accept(y)
    elif isinstance(x,list):
        for y in x:accept(y)
accept(a);accept(v);accept(c)
proposal=load(Path(a['proposal']['path']))
assert len(proposal['external_known_theorems'])==4 and all(e['imported_into_witness'] is False for e in proposal['external_known_theorems'])
main=[Path(x['path']) for x in a['sources']]+[R/x for x in ['REAPROVEITAMENTO_B6.md','REAPROVEITAMENTO_B6.json','PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json','VALIDACAO_DOCUMENTAL_B6.json','AUDITORIA_B6.json','ALVOS_B6.json','revisao_b6/REVIEW_B6_FINAL.md','revisao_b6/REVIEW_B6_FINAL.json','revisao_b6/compilation.json','run_b6_lake.py','audit_b6.py','prepare_b6_ficha.py','prepare_b6_scope.py','deliver_b6.py']]
files.update(main)
for folder in ['audit_B6','searches_B6','attempts/20260914_170651_058055']:
    files.update(p for p in (R/folder).rglob('*') if p.is_file())
stamp=datetime.datetime.now().astimezone().isoformat()
ax='\n'.join(f"| `{k}` | {', '.join(w) or 'nenhum'} |" for k,w in a['axioms'].items())
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
scope='\n'.join(f"| {e['item']} | {e['status']} | `{e['provider']}` | {e['condition']} |" for e in proposal['scope'])
bib='\n\n'.join(f"**{e['name']}** — [{e['citation']}]({e['verified_url']}). {e['exact_role']} Leitura: {e['source_read_scope']} `imported_into_witness: false`." for e in proposal['external_known_theorems'])
body=f'''[REAL — B6 pago como proposta documental tipada e auditoria de dez declarações existentes. Zero teoremas novos; hipóteses importadas e aberturas preservadas. Integração pela gerência.]

# ENTREGA 012 / B6 — importações, entradas e limites da passagem

{stamp}

**B6 acrescenta documentação de escopo e referências; não acrescenta matemática.** O auditor consulta oito teoremas e duas estruturas já construídos. A proposta JSON tem quatro referências externas com imported_into_witness=false e onze linhas de estatuto. Não foi instalada no um.py.

## Critérios da ordem

| Critério B6 | Resultado |
|---|---|
| Ficha anterior ao artefato e reaproveitamento | PAGO; dez fornecedores existentes, MD/JSON anexos; seis modalidades de busca com recortes e falhas de acesso preservados. |
| Quatro referências, exact_role e importação false | PAGO; proposta JSON com validação de esquema e campos. Leitura parcial da literatura discriminada abaixo. |
| H3 importado | PAGO como estatuto, **não como construção de H3**. the_trio_is_a_pair exige imported:H2→H3. |
| Escala de área INPUT | PAGO; newtonPlanck_equivalence e halfNat_over_two_faces_eq_quarter conferidos. Nenhum G determinado pelo kernel. |
| H_nx e w_i constante nomeados | PAGO; SectorFluid registra ambos; H_nx não foi deduzido microscopicamente. |
| Lema3 global OPEN | PAGO como delimitação; nenhuma prova local→global adicionada. |
| TGL-S versus TGL-L OPEN | PAGO como delimitação; não foi construído ou escolhido fechamento perturbativo. |
| Correções B4 preservadas | PAGO; raio no fluxo, termo Φ', suporte de densidade para igualdade, E≠0 para unicidade e constante explícita. |
| Lake próprio e axiomas | PAGO; auditor autoral e reprodução independente rc0, dez nomes existentes no trio ou sem axiomas. |
| Integração / gate / dados | NÃO EXECUTADOS, fora do escopo: proposta aditiva para gerência; campos não alterados. |

## Tabela final de estatutos

| Item | Estatuto | Fornecedor | Condição |
|---|---|---|---|
{scope}

Na linha da constante, INPUT qualifica **a escolha do caso sem constante**: a existência de Λ/C já é conclusão dos teoremas gerais, e eliminá-la exige uma condição adicional. Nas linhas REAL, o estatuto é da implicação formal com as hipóteses indicadas, não da ocorrência física de seus antecedentes.

## Referências e papel exato

{bib}

O campo KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED qualifica essas referências bibliográficas, não rebaixa os teoremas condicionais efetivamente provados em B2–B5. A extensão modificada da entropia é entrada da TGL; nenhuma citação acima a prova. Temperatura FLRW dinâmica é uma prescrição explicitada em B4, não consequência irrestrita da referência de 1977. O PDF oficial dessa referência retornou 401; a proposta não mascara a leitura parcial.

## Reprodução e alcance

Na bancada `{R}`, `run_b6_lake.py` invoca `lake build TGLExt.AuditPassageScope` na raiz kernel. Run `{a['positive_build']['path']}`, rc0, 8689 jobs, fontes idênticas antes/depois. `audit_b6.py` executou o auditor por `lake env lean`, conferiu os dez nomes, o esquema documental, as quatro importações false e a preservação das 941 fontes-base e do um.py copiado.

Revisão independente: run `{v['run']['path']}` e compilation JSON pinados. Usa sua própria raiz s, sem cópia de objetos do projeto autoral, com auditor próprio de tipos/axiomas. Mathlib e oito pacotes são caches herdados/pinados, não reconstruídos. Foram 19 fornecedores recompilados e dois auditores: 21 objetos novos, 141 no total privado. **Há diferença binária em três fornecedores — MixedLadder, SecondCone e AreaScale — embora fontes, .ilean e C gerado coincidam.** A causa de serialização não foi estabelecida; o aceite usa rc0/tipos/axiomas, sem alegação de igualdade binária integral. AuditPassageScope e outros 16 objetos coincidem com o autoral. A primeira finalização recusou a alegação mais forte e foi preservada. Nove avisos herdados permanecem; nenhum nos auditores B6. O parecer integral e binary_reproducibility_limit.json delimitam o alcance; não se confunde auditoria documental com integração no runtime.

Não foram inventados novos testes negativos para uma bibliografia. As paredes matemáticas pertinentes já foram auditadas em B4 e seus tipos foram relidos aqui; o modo importado também contém a parede existente the_pair_still_needs_its_hypotheses. Não há nova prova de existência do horizonte, traço ou testemunha global. Falhas de acesso nas buscas foram repetidas em leitura autorizada e registradas; o 401 bibliográfico permanece como limitação. Logs de avisos herdados de fornecedores não foram apagados; nenhum aviso novo é atribuído ao auditor B6.

## Axiomas dos dez nomes EXISTENTES

| Alvo | Axiomas |
|---|---|
{ax}

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
{table}

MANIFESTO_B6 e RECIBO_B6 vinculam este documento à proposta, fontes, objetos e duas auditorias. As entregas B1–B6 encerram os seis deltas desta ordem na bancada, com as correções de B4. A gerência ainda incorpora e audita a integração. A1(b) da ORDEM 011 retoma após esta entrega; seu traço concreto permanece pendente.

## Parecer independente integral

'''+(R/'revisao_b6/REVIEW_B6_FINAL.md').read_text(encoding='utf8')+'\n\n## Ficha integral anterior ao artefato\n\n'+(R/'REAPROVEITAMENTO_B6.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
m=dict(timestamp=stamp,status='B6_DELIVERED__INTEGRATION_PENDING',new_theorems=0,files=[pin(p) for p in sorted(files,key=str)])
put(R/'MANIFESTO_B6.json',json.dumps(m,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B6.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B6.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in m['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B6.json'),files=len(files)),ensure_ascii=False))
