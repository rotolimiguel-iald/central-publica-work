from pathlib import Path
import datetime, hashlib, json, os
R=Path(__file__).resolve().parent
stamp=datetime.datetime.now().astimezone().isoformat()
suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b,memory=False):
    assert p.is_relative_to(R) and b
    if p.exists():
        assert memory
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+suffix)
        bak.write_bytes(old);assert bak.read_bytes()==old and len(b)>=len(old)
    t=p.with_name(p.name+'.tmp_'+suffix);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
keys=['CORE','ABSORPTION','FOURIER','GRAPH','SPECTRAL','CALCULUS','POWERS','AFFILIATION','DUAL_SCALING']
rows=[dict(key=k,receipt=pin(R/('RECIBO_DELTA_'+k+'.json'))) for k in keys]
record=dict(timestamp=stamp,sealed=rows,author_inverse_cutoff=pin(R/'AUDITORIA_CORTES_INVERSO_A1B.json'),review_inverse_cutoff='PENDING_AT_CHECKPOINT',next='Six-mode fiche; bounded strong closedness of the full weight GNS embedding, then right action of inverse cutoffs and perturbation of the weight.',full_trace_constructed=False,gate_changed=False)
p=R/('CHECKPOINT_INVERSE_'+suffix+'.json');put(p,json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
text=f'''\n\n## Adendo {stamp} — nove deltas entregues; cortes do inverso auditados no autor

Os nove recibos deste snapshot corrigem os estados transitórios anteriores: core5, absorção6, Fourier3, grafo15, grafo espectral3, cálculo funcional5, potências4, afiliação3 e escala dual7 estão revisados e entregues no túnel. Não repetir suas compilações, nem editar os escritores de entrega. A escala dual θ_s(h)=e^(-s)h foi provada para o mesmo grafo e domínio; as potências são as de h e não uma identificação de h com Δν.

V351InverseGeneratorCutoff tem 7 teoremas e 1 definição, autor build/auditor rc0 e controle de sinal adulterado recusado. Bε=ε^-1 θ_(log ε)(R), ε>0: pertence ao core, é positivo e limitado por ε^-1; (Bε x,x−ε Bε x) pertence ao grafo de h; a equivalência inversa também foi provada. θ_s(Bε)=e^s B_(εe^s). Revisão Pasteur em curso neste checkpoint; ler o arquivo efetivo antes de entregar. Fonte final em dev_inverse_cutoff/20260914_201442_615970. Sessão autoral4408 já terminou e foi consumida.

CONSULTA_PERTURBACAO_TRACIALIDADE foi lida inteira: a próxima obrigação é a ação à direita de sqrt(Bε) no ideal nν, identificada com Jπ(sqrt(Bε))J, e depois o peso perturbado em TODO cone positivo. Não basta invariância por AdΛ para tracialidade. Não usar a inferência falsa b≤c ⇒ b*x*b≤c*x*c. A semifinitude de ν por densidade do ideal quadrado-finito já está paga; minorantes de cada positivo pertencem ao contrato final de τ, não a ν.

Fornecedores recuperados: V350ScalarRegularRightGNS e V350ScalarRegularRightPolar entregam ação direita de Λ e sua conjugação por J. V350DualOrbitStrongLimits entrega dualOrbit_factorization e continuidade forte para redes uniformemente limitadas sem restrição contável ao filtro. V350ScalarGNSStrongContinuity transporta essas redes por π. Investigar fechamento de Λν usando cortes GNS existentes antes de construir camadas novas. Uma ponte à álgebra gerada por Λ precisa fechamento forte, não somente fecho em norma de combinações de caracteres.

Snapshot: {p.name}. Todos os scripts checkpoint anteriores contêm retratos históricos e NÃO devem ser repetidos. Memória por append e backup imediato de bytes. A1(b) ativo; traço completo, A2–A7, gate e física não declarados quitados. B1–B6 e os 19 arquivos antigos permanecem intocados.
'''
md=R/'MEMORIA_RETOMADA_A1B_012.md';put(md,md.read_bytes()+text.encode('utf8'),True)
jp=R/'MEMORIA_RETOMADA_A1B_012.json';d=json.loads(jp.read_text(encoding='utf8'))
d.setdefault('append_only_checkpoints',[]).append(pin(p));put(jp,json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'),True)
print(json.dumps(dict(checkpoint=pin(p),memory=pin(md)),ensure_ascii=False))
