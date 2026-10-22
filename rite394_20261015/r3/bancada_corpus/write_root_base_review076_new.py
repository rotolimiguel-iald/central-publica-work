from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REVISOES_RAIZ_076_20260910'
assert OUT.is_dir()
pins=[]
def pin(p):
    b=p.read_bytes()
    r={'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    pins.append(r)
    return r
def new(p,text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=text.encode('utf-8')
    tmp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    tmp.rename(p)
    assert p.read_bytes()==b
    return pin(p)

note="# Revisão da raiz: mudança de base e completação076\n\n10/09/2026. [DERIVED — revisão escrita]. Li integralmente MUDANCA_BASE_E_COMPLETACAO_H3_H4.md. Não identifiquei erro material nos três resultados delimitados. Esta revisão não transporta sua conclusão finita para a classe causal completa.\n\n1. No domínio de somas separadas finitas sobre R, com s independente de B0, a decomposição de ciclos/fronteiras do complexo dinâmico prova H(C⊗A)=C⊗H(A). Os coeficientes C podem possuir relações próprias; a exatidão usa o corpo R, não uma falsa hipótese de planicidade sobre o anel de EOM. A invariância residual de Lorentz pode ser tomada depois por exatidão nos tipos localmente finitos declarados. Não se aplica esse passo a funções métricas C∞ arbitrárias sem controle de representação.\n\n2. A contração pelo jato do campo linear X_a=ax é a homotopia da ação dinâmica de Lorentz. Ela insere tanto c como seus jatos antes da avaliação na origem; na origem só os primeiros jatos são não nulos. Assim [s,ι_a]=L_a também nos jatos de c e nos antifields. Como o grupo é conectado, sua ação na cohomologia é trivial. O resultado C^G⊗H(A) usa o H dinâmico INTEIRO; não demonstra que K o gere. A naturalidade por difeomorfismos não lineares continua vindo da normalização074, não só de invariância Lorentz.\n\n3. O(4) do alvo é rígido e não recebe a homotopia da ação Lorentz. A contração ∑y0^A⊗e_A fornece o contraexemplo representacional correto à substituição de invariantes conjuntos por invariantes de cada fator. Isso não foi apresentado como classe efetiva H³.\n\n4. A família φ_b(x)=b x, com b∈SU(2), mantém a ação sigma e o tensor de matéria do habitante geométrico. Os vetores K_a(x)=T_a x são invariantes à direita e têm colchete −f_ab^c K_c; com a Maurer–Cartan esquerda η=b⁻¹db, a regra dη=−[η,η]/2 coincide com sc=c·∂c. O mapa para formas em SU(2) comuta com s em todos os campos e jatos. Os antifields podem ser postos em zero nesse mapa porque a família inteira está nas EOM. Portanto τ3 puxa o volume global da esfera e não pode ser s-exato no domínio global que a admite. Este é um teste de uma identidade global, não uma substituição do objetivo geral pelo fundo particular.\n\n5. A primitiva formal076 usa um φ0 inerte e uma vizinhança da diagonal; a órbita SU(2) inteira não pode ser inserida numa única carta formal desse domínio. Assim a não trivialidade global e a exatidão formal são compatíveis. A nota distingue corretamente M_g^K tomado antes do transporte de M_g^K já quocientado no alvo. O ciclo eliminado não é novamente um elemento não zero deste último. A paridade orientada do volume também permanece delimitada.\n\n6. A série exp(bz) prova a diferença entre cocadeias de soma separada finita e coeficientes formais conjuntos, sem alegar uma classe cohomológica ou admissibilidade causal desse exemplo.\n\n7. No quociente de EOM apenas de B0, o BRST não possui termo constante em valência normalizada: os termos KT constantes desaparecem. Os complexos truncados são então legítimos. Sobrejetividade das transições nas cocadeias permite a sequência curta com Δ(x)_N=x_N−r_Nx_(N+1). Sua sequência longa de cohomologia dá o termo lim¹ e o limite das cohomologias. A nota não presume sobrejetividade dos mapas cohomológicos. A prova usa produtos de espaços vetoriais, sem afirmar uma inversa contínua ou analítica na hierarquia de contratermos.\n\nParecer favorável às identidades e controles nessas classes. [OPEN] A classificação dos módulos das truncagens, seus mapas de transição, a geração/relacões de K, a admissibilidade de contratermos e a anomalia total permanecem abertas. A igualdade de lim¹ a zero é condição suficiente que não foi demonstrada para o sistema geral.\n\nConsulta de literatura adicional da raiz: o teorema de Anderson–Torre encontrado classifica simetrias generalizadas da gravidade de VÁCUO em quatro dimensões. Seu enunciado não é uma classificação do Einstein–sigma da bancada; não foi utilizado para declarar que nossas seis correntes são exaustivas. [Fonte primária](https://arxiv.org/abs/gr-qc/9404030).\n\nZero CAS/Lean/um.py. Fontes congeladas preservadas. Pins lidos no registro acompanhante.\n"
for rel in [
 'MUDANCA_BASE_BRST_076_20260910_024632_6031800/MUDANCA_BASE_E_COMPLETACAO_H3_H4.md',
 'MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md',
 'REVISAO_MODULOS_EBAR_076_20260910_024011_189592/PARECER_MODULOS_EBAR_076.md']:
    pin(ROOT/rel)
new(OUT/'PARECER_MUDANCA_BASE_E_COMPLETACAO_076.md',note)
for r in pins:
    b=Path(r['path']).read_bytes()
    assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
new(OUT/'REGISTRO_REVISAO_BASE_076.json',json.dumps({
 'status':'FAVORABLE_LIMITED_WRITTEN_REVIEW',
 'created_utc':datetime.now(timezone.utc).isoformat(),'files':list(pins),
 'sources_stable':True,'originals_written':False,'new_lean_compilations':0,'new_cas_controls':0
},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(pins,ensure_ascii=True))

