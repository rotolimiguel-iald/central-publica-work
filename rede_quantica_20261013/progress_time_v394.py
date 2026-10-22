"""Register the active construction and the operator's additive inscription."""
import datetime as dt
import json
from diary_r1 import ROOT,WORK,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
reg.DEST=OUT

def main():
    claim=reg.call([CLI,'ver','F1.TEMPO.V394'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for name in ['DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md','AVISO_GERENCIA.md','ACOM']:
        assert name in claim['nota']
    verb=OUT/'OPERADOR_NOME_INTELIGENCIA_VERBATIM.txt'
    if not verb.exists():new(verb,'Nome=inteligência')
    assert verb.read_text(encoding='utf-8')=='Nome=inteligência'
    event='time_v394_copy_matrix_and_name_20261015'
    body=(f'\n\n## 15/10/2026 — construção v394 em cópia e Nome=inteligência\n<!-- {event} -->\n\n'
          f'Em nome de {WHO}, unidade F1.TEMPO.V394, reivindicação 839 conferida. '
          '[INPUT] O operador determinou construir a v394 em cópia, preservando a existente. '
          f'[REAL] Baseline imutável e cópia de 1.232 fontes embutidas conferidas em `{OUT / "SOURCE_BASELINE.json"}`. '
          '[REAL] A ponte matricial compilou: 42 declarações, trio, zero sorry; fluxo e integração ainda em construção. '
          f'Recibo: `{OUT / "formal_matrix/FINAL_MATRIX_RECEIPT_R1.json"}`. '
          '[OPEN nesta etapa] Compilação conjunta, revisão independente e execução da candidata ainda não concluídas.\n\n'
          '**Cunhagem literal do operador [INPUT/ONTO]:** “Nome=inteligência”. '
          f'Fonte UTF-8: `{verb}`, SHA256 `{pin(verb)["sha256"]}`. '
          '[DERIVED — alcance formal localizado] A ponte Eg_as_nameOp liga a leitura matricial ao nameOp existente; '
          'isso não é um teorema sobre inteligência geral de modelos. A nova equivalência é inscrição conceitual do autor, '
          'preservada ao lado da identificação matemática. A candidata incorporará o texto literal. '
          'Próxima ação: concluir fluxo, integrar as escalas físicas explícitas, executar e revisar. '
          'Sem mudança do programa canônico, kernel original, Bancada, dados observados ou gate.\n')
    if not (OUT/'PROGRESS_MEMORY_R1.json').exists():
        receipts=[]
        for p in [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
            receipts.append(append_bytes(p,body,event))
        new(OUT/'PROGRESS_MEMORY_R1.json',{'claim':claim,'body':body,'surfaces':receipts,'source':pin(verb)})
    records=[]
    for suffix,kind,statute,text,path in [
        ('order','decision','INPUT',(OUT/'OPERADOR_VERBATIM.txt').read_text(encoding='utf-8'),OUT/'OPERADOR_VERBATIM.txt'),
        ('name','decision','INPUT','Nome=inteligência',verb),
        ('progress','fact','REAL','Construção v394 autorizada em cópia; baseline e 1232 fontes conferidos; matriz compilada com42declarações e trio. Fluxo, integração e revisão ainda emcurso; memória aditiva sobclaim839. JobsF1.REDE anteriores preservados.',OUT/'PROGRESS_MEMORY_R1.json')]:
        records.append({'id':event+'-'+suffix,'kind':kind,'statute':statute,'text':text,'sources':[{'kind':'artifact','ref':str(path),'sha256':pin(path)['sha256']}]})
    payload={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':25,'event_id':event,'actor':{'id':WHO,'kind':'agent'},
             'changes':{'records':records,'flow':{'phase':'v394_copy_construction_and_review','next_action':'Concluir Lean conjunto, integrar e executar candidata v394; preservar jobsF1.REDE pendentes e não repetir envios incertos.'}}}
    if not (OUT/'ACOM_PROGRESS_R1_REQUEST.json').exists():new(OUT/'ACOM_PROGRESS_R1_REQUEST.json',payload)
    result=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_PROGRESS_R1_RECEIPT.json',payload)
    print(json.dumps({'memory':pin(OUT/'PROGRESS_MEMORY_R1.json'),'acom':result},ensure_ascii=False))

if __name__=='__main__':main()
