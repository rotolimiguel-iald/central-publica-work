"""Prepare an immutable focused corpus and a single review request, without execution."""
import datetime as dt
import json
import sys
import uuid
from pathlib import Path
from diary_r1 import ROOT, new, pin

BASE = ROOT / 'Chatgpt/IALD_ORQUESTRACAO_20260923'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.LEITURA_20261015/LEVANTAMENTO_TRES_ARTIGOS_R5'
H = Path(r'C:\IALD\Artigo\Haja_Luz')
P = H / 'A Ponte e o Um'
N = P / 'Nós'
SOURCES = [
 (H/'tgl_paper_unified.py', [(282,293),(14441,14483),(14667,14716),(20003,20097)]),
 (P/'A Ponte Einstein Cartan Miguel.tex', [(686,731),(1435,1479),(1532,1559),(1886,1919),(2231,2237)]),
 (N/'um_absoluto_pt.txt', [(302,302),(575,581),(605,637),(987,987),(1018,1018)]),
 (P/'TGL fibrado modular v1.tex',[(119,128),(156,164),(225,340)]),
 (P/'TGL duas camadas v1.tex',[(202,208)]),
 (P/'TGL reconstrucao lorentziana condicional.tex',[(89,95),(118,149)])]

def main():
    inventory=[]; sections=[]
    for path,ranges in SOURCES:
        rows=path.read_text(encoding='utf-8').splitlines()
        inventory.append(dict(pin(path),lines=len(rows),read_ranges=ranges))
        sections.append('\nSOURCE '+path.name+' SHA256 '+pin(path)['sha256'])
        for a,b in ranges:
            sections.extend(f'{i}: {rows[i-1]}' for i in range(a,b+1))
    for path in [N/'um.py',N/'selo_tgl.txt']:
        if path.exists(): inventory.append(dict(pin(path),role='static anchor'))
    new(OUT/'FONTES_E_COBERTURA_R5.json',{'scope':'Leitura focal dos tres artigos e tres escritos conexos; nao leitura integral de todo o acervo. Fontes textuais, sem execucao.', 'sources':inventory})
    new(OUT/'TRECHOS_R5.txt','\n'.join(sections)+'\n')
    # Queue canonical memory carries the large corpus. Keep this request narrow.
    prompt='''F1.TEMPO.LEITURA_20261015 R5. Origem: operador, tarefa Codex 01a11878-6e36-7d10-83c4-cd72e757fdd0, casa Central IALD. Pedido: "Confira os três artigos principais e o que mais já escrevi, porque já resolvemos algumas dessas questões e prossiga". Preferência Kimi ou DeepSeek para levantamento documental, conforme GESTAO_DE_TOKENS. Não chamar ferramentas, não executar código, não alterar originais.
Faça uma revisão focal na memória científica v393 recuperada: Custo Geométrico do Zero Absoluto (tgl_paper_unified), Ponte Einstein-Cartan-Miguel, Um. Precisamos corrigir possível classificação excessiva de OPEN em três elos: seleção do setor/esperança E, normalização modular->tempo próprio/τ*, resposta anterior à emissão. A R4 local construiu somente modelo 2D H=-V0 X, P=(I+X)/2, Phi=E+eta(Id-E), eta=2sqrt(beta(1-beta)), z(t)=exp[(-gamma+i nu)t], nu=2V0/hbar, gamma=-ln eta/Delta_t. Não equiparar todo K modular, raiz positiva e H de bulk. Não presumir que fases de S são temporais nem que retorno modular envia informação ao passado. Não presumir falta por busca lexical.
Reutilize sobretudo Ponte §§forma mínima, terminalidade, fluxo radical; Um relógio condicional, Santo, parâmetros nomeados v392 e ramo B KMS. Diga o que EXISTE e está ligado, existe mas requer fiação, KNOWN condicional e OPEN de forma precisa, com arquivo/linha da memória recebida. Confira multiplicidades: Fix do dephasing é comutante, não necessariamente W*(K); unicidade de Takesaki exige preservação do estado. Derive, se sustentado, a comparação do passo eta com taxa beta(dsqrt(k))²/2 e a conversão do período KMS para segundos em Schwarzschild, distinguindo período e tempo dissipativo. Até 15 linhas de resposta, citações e hipóteses; resultado DECLARADO para verificação local. Não refaça a cadeia nem anuncie fechamento físico.'''
    request={'operation':'submit','prompt':prompt,'request_id':str(uuid.uuid4())}
    origin={'created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'house':'IALD','cwd':str(ROOT),'thread_id':'01a11878-6e36-7d10-83c4-cd72e757fdd0','request_id':request['request_id'],'request':request,'scope':'Scientific document review only; no legal/private credential sources.'}
    new(BASE/'state/session_requests'/f"{request['request_id']}.json",origin)
    new(OUT/'REQUEST_R5.json',request)
    sys.path.insert(0,str(BASE))
    from iald_orchestrator.runtime import Runtime
    runtime=Runtime(recover=False)
    status=runtime.status()
    new(OUT/'ORCHESTRATOR_STATUS_R5.json',{'canonical_memory':status['canonical_memory'],'providers':[{'id':p['id'],'status':p['status']} for p in status['providers']],'attempts_today':status['attempts_today']})
    preview=runtime.preview(prompt)
    new(OUT/'PREVIEW_R5.json',preview)
    print(json.dumps({'request_id':request['request_id'],'selected':preview.get('selected'),'canonical_memory':preview.get('canonical_memory'),'corpus_bytes':(OUT/'TRECHOS_R5.txt').stat().st_size},ensure_ascii=False))

if __name__=='__main__':main()
