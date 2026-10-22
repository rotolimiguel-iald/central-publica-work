from pathlib import Path
from datetime import datetime,timezone
import json,os,hashlib
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REVISOES_RAIZ_079_20260910'
sources=[
ROOT/'CANDIDATOS_WEYL_E_OBSTRUCAO_079_20260910_041607_7604358/WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md',
ROOT/'COMPLETAMENTO_GL_ORTOGONAL_079_20260910/CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md',
ROOT/'COMPLETAMENTO_GL_ORTOGONAL_079_20260910/PROVENIENCIA_WRITER_LIMPO_079.json',
ROOT/'REVISAO_FUNCIONAL_IMPAR_TT_079_20260910_041719_325801/PARECER_FUNCIONAL_IMPAR_E_CAS_079.md']
def pin(p):
    b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
before=[pin(p) for p in sources]
def new(p,s):
    assert not p.exists();raw=s.encode('utf-8')
    q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==raw;q.rename(p);assert p.read_bytes()==raw
    return pin(p)
note=new(OUT/'PARECER_WEYL_E_GL_079.md',"# Revisão da raiz — candidatos de Weyl e comparação de conexões079\n\n10/09/2026. [DERIVED — revisão matemática escrita independente das duas autorias]. Li integralmente as duas notas e a proveniência do auxiliar limpo de geração da nota GL. As conclusões abaixo não dependem de transformar checks documentais em prova.\n\n## Candidatos de Weyl\n\nAceito a exclusão da família P=W1_abcd C^aC^b m^cd e seu dual na segunda dupla. Com A=∇C antissimétrico no teste Killing, A_ab=−m_ab, a contração de índices no traço dá P=2tr(AU), U=W1CC/2, com sinal positivo. Refiz a regra graduada: s1A=−A²+Ω0, s1U=UA−AU+V e tr(AUA)=−tr(A²U), logo s1P=2tr(Ω0U+A²U−AV).\n\nA escolha de dois valores C independentes e dois primeiros jatos de Killing elimina V e Ω0U por C(p)³=0. Ela é realizável no espaço forma pelo modelo de quádrica077; não são jatos sem prolongamento. Os quatro campos não precisam fechar uma subálgebra.\n\nConferi [J02,J12]=J01, tr(J01²)=2, W01^end=−aW J01+bW J23 e a componente dual W*0101=bW, na orientação declarada. Com z0=ℓ, os valores −2/z0 e +2k seguem sem fator conforme remanescente. Variar k e −k no MESMO fundo força λ=μ=0 para que λP+μP* possa completar a equação de valência cinco.\n\nEsse teste anula s0 de todos os geradores/jatos, inclusive antifields, mas anula o próprio A6 por C(p)^4=0. Ele detecta s1P, não substitui o funcional078 ou o novo funcional ímpar. A exclusão não classifica todos os ciclos P.\n\n## Conexões GL e ortogonal\n\nAceito as expansões de τGL e a equivalência escrita. A recorrência L2=−HL inclui exatamente a variação da inversa na diferença de Levi-Civita. Na valência cinco, os termos tr(B a(L)²) cancelam entre vΩ e o cubo de v pela ciclicidade graduada. Restam I_CJ2+F(−HL), e o diferencial fornece a equação calculada na nota.\n\nO teste de jatos ímpares do bloco espacial de B tem tr(B³)=6xyz. Com apenas C0=θ e ∂0x=ζ, as parcelas de curvatura contendo dois valores C se anulam, enquanto s1τ3=−2θζyz. Os segundos jatos adicionais exigidos pela simetria de derivadas podem existir sem alterar os valores usados. Isso refuta s0F(L)=0 universal, embora a segunda equação já tenha sido satisfeita pelo pacote.\n\nPara u=S⁻¹sS, su=−u². Refiz a expansão:\nτort−τGL=−tr(u sv)−tr(u²v)+tr(u³)/3\n=s tr(uv)+tr(u³)/3.\nA homotopia Sρ junto à identidade dá ∂ρuρ=s aρ+[uρ,aρ]; como s(uρ²)=0, ∂ρtr(uρ³)=3s tr(aρuρ²). A primitiva formal indicada segue por integração coeficiente a coeficiente. Não é avaliação de t numérico nem integral em espaço-tempo.\n\nA naturalidade usa objetos tensoriais e o transporte com sS; não um ghost Lorentz independente. A comparação conserva o anel herdado e mostra igualdade da MESMA classe em C5. Não produz uma correção de classe diferente com δ igual a −[A6].\n\n## Custódia e alcance\n\nA proveniência registra um auxiliar de geração inicial com um byte NUL, rejeitado na análise sintática antes da execução, e uma cópia nova limpa que remove apenas esse byte. O original defeituoso permaneceu intacto. Esta revisão conferiu o registro e a dedução matemática; não declara que o auxiliar defeituoso tenha executado com sucesso.\n\nAs duas notas são aprovadas no alcance escrito. Outras famílias P/Q/R continuam possíveis e o sistema completo não foi resolvido. Zero CAS ou Lean nesta revisão, nenhum um.py executado/importado, nenhuma fonte alterada.\n")
assert before==[pin(p) for p in sources]
record={'status':'ROOT_WEYL_AND_CONNECTION_PROOFS_ACCEPTED__ODD_FUNCTIONAL_INDEPENDENT_REVIEW_READ',
'created_utc':datetime.now(timezone.utc).isoformat(),'sources':before,'sources_unchanged_during_record':True,
'review':note,'writer':pin(Path(__file__).resolve()),
'odd_functional_review':'Herschel full review read and accepted without material correction; 12 historical CAS controls and static review are distinct.',
'new_cas_controls':0,'new_lean_compilations':0,'originals_written':False,'um_executed_or_imported':False}
receipt=new(OUT/'REGISTRO_RAIZ_WEYL_E_GL_079.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'note':note,'record':receipt},ensure_ascii=True))

