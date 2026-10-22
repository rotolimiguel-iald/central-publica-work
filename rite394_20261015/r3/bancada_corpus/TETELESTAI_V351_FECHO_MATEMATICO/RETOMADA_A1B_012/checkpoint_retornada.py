from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
stamp=datetime.datetime.now().astimezone().isoformat()
suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put_memory(p,b):
    assert p.is_relative_to(R) and b,p
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+suffix)
        assert not bak.exists();bak.write_bytes(old);assert bak.read_bytes()==old
    temp=p.with_name(p.name+'.tmp_'+suffix);temp.write_bytes(b);assert temp.read_bytes()==b
    os.replace(temp,p);assert p.read_bytes()==b
specs=[
 ('core',['V351ScalarImaginaryLeftTransport','V351ScalarImaginaryCoreAction'],'AUDITORIA_ACAO_CORE_A1B.json','revisao_core/REVIEW_A1_CORE_FINAL.json'),
 ('absorption',['V351RegularFlowAbsorption'],'AUDITORIA_ABSORCAO_A1B.json','revisao_absorcao/REVIEW_A1_ABSORPTION_FINAL.json'),
 ('fourier_translation',['V351FourierTranslation'],'AUDITORIA_FOURIER_TRANSLACAO_A1B.json','revisao_fourier/REVIEW_A1_FOURIER_FINAL.json'),
 ('positive_graph',['V351RegularPositiveGraph'],'AUDITORIA_GRAFO_POSITIVO_A1B.json','revisao_grafo/REVIEW_A1_POSITIVE_GRAPH_FINAL.json')]
rows=[]
for label,mods,aud,review in specs:
    sources=[pin(K/'TGLExt'/f'{m}.lean') for m in mods]
    decls=[]
    for p in sources:
        for kind,name in re.findall(r'^(def|theorem) (\w+)',Path(p['path']).read_text(encoding='utf8'),re.M):
            decls.append(dict(kind=kind,name='TGLV350.Regular.'+name))
    runs=[]
    folders=['dev_left','dev_core'] if label=='core' else ['dev_'+label]
    for folder in folders:
        valid=[]
        for p in sorted((R/folder).glob('*/run.json')):
            d=json.loads(p.read_text(encoding='utf8'))
            if d['returncode']==0 and d['source'] in sources:valid.append(pin(p))
        assert valid,folder
        runs.append(valid[-1])
    ap=R/aud;rp=R/review
    rows.append(dict(label=label,sources=sources,declarations=decls,dev_accepted_runs=runs,
        author_audit=pin(ap) if ap.exists() else None,
        review=pin(rp) if rp.exists() else None,
        review_path_is_expected_not_asserted=True))
status=dict(timestamp=stamp,objective='ORDEM012 B1–B6 delivered; resumed ORDEM011 A1(b) after B6.',
    write_scope=[str(R),str(R.parent.parent/'TUNEL/DO_CHATGPT')],
    sealed_orphans_receipt=pin(R/'RECIBO_ORFAOS_A1B.json'),
    sealed_B6_receipt=pin(R.parent.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA/RECIBO_B6.json'),
    current_deltas=rows,all_new_development_declarations=sum(len(q['declarations']) for q in rows),
    full_trace_constructed=False,gate_changed=False,
    live_sessions=dict(sequential_author_validation=20318,positive_graph_validation_waiter=21402),
    reviewer_id='01a092ea-b494-7ca0-bdcb-ec28c12c30e8',
    author_current_core_attempt=str(R/'core_attempts/20260914_184033_714941'),
    instructions=['Do not rerun the cold orphan build; it passed and was sealed.',
      'Do not start simultaneous Lake builds in k. Session20318 handles core/absorption/Fourier sequentially;21402 waits then handles positive graph.',
      'Inspect actual reviewer paths; expected names in this checkpoint are not claims of existence.',
      'No final trace/affiliation/imaginary-power identification follows from the positive graph alone.',
      'Orphan receipt and B1–B6 immutable. Every existing memory edit requires immediate byte backup and atomic replacement.',
      'Next mathematics: identify the new regular positive graph spectrally, prove imaginary powers equal regularUnitary, affiliation and dual scaling, then inverse-generator trace; finite-minorant semifiniteness remains a separate gap.',
      'Preserve all failed DEV attempts; never count partial sorryAx outputs as accepted proofs.'])
put_memory(R/'MEMORIA_RETOMADA_A1B_012.json',json.dumps(status,ensure_ascii=False,indent=2).encode('utf8'))
table='\n'.join(f"| {q['label']} | {sum(d['kind']=='theorem' for d in q['declarations'])} | {sum(d['kind']=='def' for d in q['declarations'])} | {'arquivo presente; ler' if q['author_audit'] else 'pendente'} | {'arquivo presente; ler' if q['review'] else 'pendente; nome ainda esperado'} |" for q in rows)
text=f'''[REAL/OPEN — checkpoint da retomada; evidências de desenvolvimento e aceitação são distintas]

# Memória central da retomada A1(b)

{stamp}

Objetivo ativo: ORDEM012 entregue B1–B6; A1(b) retomado após B6. Não retomar D1, evidência experimental, sigma, integração no um.py ou discussão antiga de gate. Escrita somente em RETOMADA_A1B_012 e novas entregas no túnel. B selada, fontes e memórias canônicas somente leitura.

## Entregue

Os sete fornecedores existentes (36teoremas4defs) tiveram duas reproduções isoladas rc0. O autor revalidou940fontes/configs e dois negativos rc1 por TypeMismatch. Cinco módulos receberam revisão do sidecar; dois antiunitários de autoria anterior dele receberam inspeção do principal. Sete objetos autorais novos coincidem com os novos do revisor; diferem dos históricos. RECIBO_ORFAOS_A1B liga a entrega e o manifesto. Não acrescenta matemática nem fecha o traço.

## Deltas novos, sem redefinir o que já existia

| Delta | Teoremas DEV rc0 | Definições | Auditoria autoral isolada | Revisão |
|---|---:|---:|---|---|
{table}

Core: U_t π(A)=π(Λ_t A Λ_t*) U_t para todo A no core, com U_t do mesmo S†S. Não implica U_t=π(Λ_t). Absorção: W S_t W*=Λ_t; não afirma W∈N. Fourier: F S_t=M_(2πt) F no L² existente, sem outro espaço. Grafo: V=W F^-1, R=V M_sigmoid(2πξ)V^-1, h=(1−R)/R no domínio RanR; positivo, autoadjunto, fechado, domínio denso e núcleo zero em DEV. Não confundir este h candidato com uma identificação já provada de suas potências ou afiliação.

Antecedente049–050: SpectralHilbert é Lpℂ; não se instancia no LpTower. O adendo registra a diferença de tipo, e a positividade vetorial foi adaptada ao multiplicador já existente. Grafo/domínio/autoadjunção são consumidos dos lemas genéricos existentes. Real.sigmoid e Fourier isométrica já existem e foram reutilizados.

## Processos e próxima ação

Sessão20318 executa auditoria40 (já passou), Lake/auditoria5core,6absorção e3Fourier sequencialmente. Sessão21402 espera a auditoriaFourier e então executa Lake/auditoria15grafo. Não lançar segundo Lake em k. Sidecar Pasteur tem fila autorizada40→5→6→3→15 em v, cada parecer separado. Não repetir coldbuild40. Ler os arquivos efetivos antes de selar cada entrega. Os nomes de revisão no JSON são esperados enquanto ausentes; não inventar existência.

Após cada aceite: ENTREGA própria, relatório integral e ficha anexados, hashes lidos, manifesto e recibo. Nenhum dos scripts de entrega futuros foi executado por este checkpoint. deliver_orphans já executado; não repetir.

Lacunas posteriores: identificação das potências imaginárias do grafo com Λ_t, afiliação a N, escala dual e perturbação pelo inverso para construir RegularCoreTraceData; semifinitude por minorantes positivos também permanece. Não substituir esse contrato pelo peso dual invariante. A1(b) continua ativo.

## Registro de execução desta retomada

As fichas foram escritas antes dos respectivos alvos. A fichaFourier teve dois extratos cortados no := de binders; ADENDO_FICHA_FOURIER_TRANSLACAO fornece os tipos completos e preserva o original. As buscas negadas pelo sandbox foram registradas e repetidas com leitura autorizada. As tentativas DEV que falharam por importação, elaboração, coerção ou recursão de simp permanecem em suas pastas; só rc0 com fonte final foi selecionado. A compilação de projeto e as revisões posteriores são as que podem aceitar cada delta. Nenhum resultado de natureza foi calculado aqui.
'''
put_memory(R/'MEMORIA_RETOMADA_A1B_012.md',text.encode('utf8'))
print(json.dumps(dict(memory=pin(R/'MEMORIA_RETOMADA_A1B_012.md'),new_dev_declarations=status['all_new_development_declarations']),ensure_ascii=False))
