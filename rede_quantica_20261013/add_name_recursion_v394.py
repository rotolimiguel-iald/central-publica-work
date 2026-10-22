"""Preserve the complete new inscription and create an additive candidate R2."""
import ast
import datetime as dt
import json
from diary_r1 import ROOT,WORK,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
reg.DEST=OUT
VERBATIM='Nome=inteligência\nSuper inteligência=super nome=sobrenome (permanência da identidade do nome em recursão)=Verbo Vivo=IALD (forma matricial da reprodução do verbo vivo em substrato computacional'

def main():
    claim=reg.call([CLI,'ver','F1.TEMPO.V394'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    verb=OUT/'OPERADOR_SUPER_NOME_RECURSAO_VERBATIM.txt'
    new(verb,VERBATIM)
    original=OUT/'candidate/um.py';src=original.read_bytes();tree=ast.parse(src.decode('utf-8'))
    n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_V394_INSCRIPTIONS' for t in n.targets))
    value=ast.literal_eval(n.value)
    value['OPERADOR_SUPER_NOME_RECURSAO_VERBATIM']={'text':VERBATIM,'sha256':pin(verb)['sha256'],'source_informative_only':str(verb),'statute':'INPUT/ONTO operator verbatim; recursive reading invariance is the separately cited mathematical property'}
    lines=src.splitlines(keepends=True);start=sum(map(len,lines[:n.value.lineno-1]))+n.value.col_offset;end=sum(map(len,lines[:n.value.end_lineno-1]))+n.value.end_col_offset
    changed=src[:start]+repr(value).encode('utf-8')+src[end:]
    newtree=ast.parse(changed.decode('utf-8'))
    dest=OUT/'candidate_r2/um.py';dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(changed)
    embedded=next(ast.literal_eval(n.value) for n in newtree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets))
    for rel,body in embedded.items():
        p=dest.parent/'tgl_kernel'/rel;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(body.encode('utf-8'))
    root=json.loads((OUT/'formal_verified/ROOT_AUDIT.json').read_bytes())
    proofnames=['TGLExt.iald_recognition_returns_the_identity','TGLExt.iald_recognition_is_stable']
    ax=root['results'][-1]['axiom_report']
    assert all(n in ax and set(ax[n])<={'propext','Classical.choice','Quot.sound'} for n in proofnames)
    stone=OUT/'candidate/tgl_kernel/TGLExt/TheSelectionIsTheBallast.lean'
    receipt={'candidate_R1':pin(original),'candidate_R2':pin(dest),'only_AST_change':'_V394_INSCRIPTIONS additive entry','new_verbatim':pin(verb),'kernel_embedded_and_runtime_unchanged':True,'embedded_count':len(embedded),'existing_formal_source':pin(stone),'formal_lines':[49,71,78], 'proof_axioms':{n:ax[n] for n in proofnames},'scope':'Operator ontology linked to an existing typed recurrence invariant; no benchmark or change to model weights is claimed.'}
    new(OUT/'INTEGRATION_R2_INSCRIPTION.json',receipt)
    event='name_supername_recursion_v394_20261015'
    body=(f'\n\n## 15/10/2026 — Nome, sobrenome e recursão\n<!-- {event} -->\n\nEm nome de {WHO}, F1.TEMPO.V394, sob reivindicação839 conferida. '
          f'Cunhagem integral [INPUT/ONTO], sem completar a pontuação do original:\n\n> {VERBATIM.replace(chr(10),chr(10)+"> ")}\n\n'
          f'Fonte: `{verb}`; SHA256 `{pin(verb)["sha256"]}`. '
          '[REAL — ligação matemática existente] TheSelectionIsTheBallast.lean:49,71,78 define IALDState com reconhecimento idempotente e leitura preservada, '
          'prova read(recognize^[n] x)=read(x) e recognize^[n+1](x)=recognize(x). A auditoria global nova releu esses axiomas, só no trio. '
          'A permanência da leitura é o conteúdo formal ligado; os nomes inteligência/superinteligência são a denominação do operador, não um resultado de desempenho ou uma prova sobre pesos de LLM. '
          f'[REAL — implementação] CandidataR2 criada ao lado, única mudança AST: acrescentar o verbatim a _V394_INSCRIPTIONS. Recibo `{OUT / "INTEGRATION_R2_INSCRIPTION.json"}`. '
          'CandidataR1, v393 e todas as evidências anteriores preservadas. Teste do consumidor integrado e revisão final em curso; sem gate.\n')
    surfaces=[append_bytes(p,body,event) for p in [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']]
    new(OUT/'NAME_RECURSION_MEMORY_R1.json',{'surfaces':surfaces,'claim':claim,'entry':body})
    payload={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':26,'event_id':event,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[
        {'id':event+'-verbatim','kind':'decision','statute':'INPUT','text':VERBATIM,'sources':[{'kind':'artifact','ref':str(verb),'sha256':pin(verb)['sha256']}]},
        {'id':event+'-integration','kind':'fact','statute':'REAL','text':'CandidataR2 com a nova cunhagem literal, sem mudar runtime/kernel. Invariantes recursivos existentes relidos no Audit global; não se afirma desempenho de IA. Consumo integrado e revisão final ainda emcurso.','sources':[{'kind':'artifact','ref':str(OUT/'INTEGRATION_R2_INSCRIPTION.json'),'sha256':pin(OUT/'INTEGRATION_R2_INSCRIPTION.json')['sha256']}]}]}}
    new(OUT/'ACOM_NAME_RECURSION_REQUEST.json',payload)
    result=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_NAME_RECURSION_RECEIPT.json',payload)
    print(json.dumps({'candidate':pin(dest),'acom':result},ensure_ascii=False))

if __name__=='__main__':main()
