from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REVISOES_RAIZ_086_20260910'
assert not OUT.exists()
OUT.mkdir()

def pin(p):
    raw=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def new(p, text):
    raw=text.encode('utf-8')
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    temp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    temp.rename(p)
    assert p.read_bytes()==raw

paths=[
 'SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md',
 'REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md',
 'CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md',
 'REVISAO_CORRENTES_UMA_DERIVADA_086_20260910_065540_575112/PARECER_CLASSIFICACAO_E_NORMALIZACAO_086.md',
 'PONTRYAGIN_CARACTERISTICO_E_LIMITE_BBH_086_20260910_062514_4956488/NAO_EXATIDAO_INVARIANTE_E_LIMITE_DA_IMPORTACAO_BBH.md',
 'REVISAO_PONTRYAGIN_CARACTERISTICO_086_20260910/PARECER_TRANSGRESSAO_GL_E_CONTRATO_CARACTERISTICO_086.md',
 'INSPECAO_CANONICO_NAVEGACAO_086_20260910/PARECER_INSPECAO_CANONICA_086.md',
]
before=[pin(ROOT/p) for p in paths]
text='''# Conferência da raiz086 — símbolo, correntes e transgressão

10/09/2026. [DERIVED — revisão matemática escrita]. Li integralmente as três notas086 abaixo e seus três pareceres independentes. Aproveitei a leitura anterior da nota característica após a compactação, reli as outras duas e todos os pareceres. Reconstituí os elos descritos a seguir; não identifiquei erro material no alcance declarado. Minha própria dedução dos corolários CE/cúbicos é outra fonte, submetida a Singer e não aprovada por este parecer da raiz.

## 1. Estriteza e injetividade da divergência

A nota de Herschel e a revisão de Turing pagam o elo que faltava às tentativas por corrente: o símbolo curvo não é substituído pelo plano por continuidade em K. Se PHh tem ordem baixa por cancelamento superior, σPσH=0 dá σP=σBD; retirar BD mantém PH porque DH=0 e baixa a ordem de P. A indução finita prova estriteza da imagem das EOM, incluindo seus possíveis cancelamentos inferiores. O grau de K é zero nessa filtração, pois ele é um real fixado.

Conferi que a filtração INDUZIDA no submódulo gauge-fechado preserva a injeção de graduados. Retirar uma EOM conserva o fechamento porque HR₀=0. A derivada respeita esse submódulo/ideal e seu símbolo é a derivada plana em todos os índices. Por isso temos uma injeção que entrelaça divergências; só uma injeção de representações não seria suficiente.

Na potência simétrica, a ordem é a SOMA das ordens dos fatores. O módulo plano possui os tipos (r+4,r) e (r,r+4), com pesos 2j. Refiz a contagem: um vetor (1,1) exige ordens r e r+1 na mesma quiralidade; os tipos cruzados exigiriam duas desigualdades incompatíveis. Há duas cópias vetoriais complexas por grau 2r+5, e nenhuma em grau menor que cinco.

A realização métrica plana é necessária e está dada. A polarização h=λλ ξ'ξ' exp(ipx)/[λ'ξ']² é TT e nula em momento, produz Weyl puramente de uma quiralidade. A soma de duas ondas da mesma quiralidade, com AMBOS os brackets não nulos, faz a contração escalar S_r e □S_r não nulas. As quiralidades são separadas escolhendo apenas ondas de uma delas. Assim o gradiente gera cada cópia, e suas divergências são independentes. A complexificação testa identidades polinomiais reais; não se afirma estado físico complexo.

O maior símbolo de qualquer corrente curva não nula tem, portanto, divergência não nula um grau acima. Essa divergência começa em grau seis, enquanto J_W tem símbolo de grau quatro não nulo. Isto exclui divV=J_W para TODAS as ordens finitas e também prova núcleo zero da divergência nesse espaço. As extensões escalares são de mapas reais fixados; planura sobre R cobre nilpotentes sem avaliá-los numericamente.

Consultei novamente as duas primárias no alcance preciso: [Khavkine, §3.1, fórmulas32](https://arxiv.org/pdf/1805.03751) para o complexo de compatibilidade Killing/curvatura/Bianchi, e [Anco–Pohjanpelto, fórmulas2.1–2.7](https://arxiv.org/pdf/math-ph/0202019) para os jatos simetrizados do sistema plano e sua derivação total. A conta de duas ondas estabelece a realização métrica necessária aqui. Não importei a classificação de correntes com Killing externo, nem liberdade da torre curva.

## 2. A classificação com uma derivada oferece uma verificação distinta

A nota de Singer e o parecer de Herschel usam a definição I=(1/2)W²; a fonte082 usava W². A relação correta é I082=2I086, com J idêntico. A notação de spins da nota de uma derivada usa j, enquanto a prova simbólica usa 2j; convertidos esses rótulos, ambas dão exatamente duas correntes reais: A gradI+B gradJ.

Conferi as constantes diretamente nas fórmulas TT. Para k=0, p=(z/z₀)² e I=2z⁶/(ell⁴z₀⁴), dando I'=12/z₀³ e □I=−36/z₀⁴ após ell=z₀. Com k=1/z₀, J'=−24/z₀³ e □J=56/z₀⁴. Isso prova independência dos dois gradientes e divergências por fatores reais invertíveis em Rher.

O alvo ímpar força B=−z₀²/14 em k=1/z₀, mas B=z₀²/28 em k=2/z₀. Com f invariante permitido, diferenciar elimina f e a diferença dos testes dá 3312B/z₀⁵=0, ainda incompatível com J' não nulo. K permanece fixado durante a derivação. Essas são contas escritas; não executei CAS nem reapresentei controles083 como execuções086.

Esse argumento específico dispensa a nulidade N₂^g085 e não serve, sozinho, para todas as ordens. A prova geral acima paga a ampliação em arquivo distinto. A nota de uma derivada conserva legitimamente seu alcance local histórico.

## 3. A transgressão ordinária não contradiz o resultado

A nota de Turing e o parecer de Singer preservam a diferença de categorias. No MESMO fibrado tangente, a diferença GL entre conexões sem torção satisfaz A^a_b∧e₀^b=0. Na espaço-forma isso anula tr(A R₀) e dá d tr(L DbarL)=tr(W₁²) no coeficiente quadrático, off-shell.

Essa primitiva não pertence ao espaço de correntes gauge-invariantes do quociente Weyl/EOM. A avaliação local de sua variação, realizada com a solução TT k=0 rotacionada, dá −1/(4z₀) na componente023. A deformação de gauge tem valor e primeiro jato zero, segundo jato escolhido e terceiro zero, de modo que é compatível com os comutadores. Somar EOM não remove o defeito. A liberdade de somar uma corrente ordinária fechada é diferente; a prova por símbolo decide a impossibilidade de uma primitiva invariante finita.

A sequência curta de complexos A→B→B/A fornece o critério de imagem correto, mas sua exatidão sozinha não calcula essa imagem. Também não basta importar não trivialidade característica no grau máximo de outra teoria ou trocar K fixado por K=0: os contraexemplos algébricos da nota demonstram essas limitações. A prova086 por estriteza é a comparação adicional efetivamente realizada.

## 4. Estado e limites

[DERIVED] As três notas são compatíveis e têm revisões específicas. O resultado novo consolidável é a impossibilidade de cancelar J_W por uma corrente natural quadrática FINITA no contrato fixado, com injetividade da divergência. A consequência para os mapas BRST está escrita separadamente e passa por revisão independente própria.

[REAL — leitura] O novo parecer canônico086 e o snapshot de Singer continuam em v338 nos caminhos conferidos, sem delta de bytes nos quatro artefatos. A conclusão limita a atualização efetivamente localizada; não nega existência de outra cópia em preparação. Presença AST77/98 não é compilação nova.

[OPEN] Grupos BRST completos, termos líderes posteriores, todos os alvos do limite inverso, matéria/sigma física não constante, admissibilidade causal, QME, UV e reconstrução gravitacional geral pelos mesmos dados. Ghost quatro não é anomalia física de ghost um. Fase/ramo e H3 da tela permanecem reconhecidos.

[REAL — custódia] Este recibo mede as fontes antes/depois da emissão nova. Não é auditoria recursiva de todas as dependências históricas. Nenhum original, Atlas, índice, memória canônica, um.py, selo ou gate foi alterado. Zero nova execução matemática, CAS, Lean ou natureza. A investigação087 não é um resultado desta entrega.
'''
new(OUT/'PARECER_SIMBOLO_TRANSGRESSAO_E_CORRENTES_086.md',text)
after=[pin(ROOT/p) for p in paths]
assert before==after
record={'created_utc':datetime.now(timezone.utc).isoformat(),'sources':before,
        'source_pins_unchanged':True,'review':pin(OUT/'PARECER_SIMBOLO_TRANSGRESSAO_E_CORRENTES_086.md'),
        'helper':pin(Path(__file__).resolve()),'new_mathematical_executions':0,
        'new_cas_executions':0,'new_lean_compilations':0,'originals_written':False,
        'scope':'Written root review of other authors, not approval of root corollaries.'}
new(OUT/'REGISTRO_REVISAO_RAIZ_086.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review':record['review'],'sources':len(before)},ensure_ascii=True))
