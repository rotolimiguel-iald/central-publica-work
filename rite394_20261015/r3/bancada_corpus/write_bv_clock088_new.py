from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'HOMOTOPIA_BV_RELOGIOS_088_20260910'
assert not OUT.exists()
OUT.mkdir()
sources={
 'free':'EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md',
 'bv':'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
 'causal':'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
 'norm':'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
 'nat':'NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md',
 'descent':'DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md',
 'rees':'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
 'h4':'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
 'h4review':'REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md',
 'prior':'REEXAME_SUFICIENCIA_087_20260910/RESULTADO_ENTREGA_087.json'
}
pins=[]
for p in sources.values():
    path=ROOT/p; raw=path.read_bytes()
    pins.append({'path':path.as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
def L(key,label):
    return '['+label+'](<'+(ROOT/sources[key]).as_posix()+'>)'

body=r'''# Homotopia BV por relógios no fundo físico — 088

10/09/2026. /root. [DERIVED — demonstração escrita nova, sujeita a revisão independente]. [REAL — pins documentais].

**Resultado:** no fundo físico Einstein–sigma de069, a inversa local de gauge já construída em068 permite anular construtivamente a cohomologia BRST clássica de ghost positivo e a cohomologia total de grau maior que quatro, na completação formal com coeficientes LOCALIZADOS onde os relógios têm posto completo. A prova inclui todos os antifields. Dá uma recorrência de primitivas, não uma solução da QME.

**A categoria importa:** essa localização usa inversas de jatos de fundo excluídas do contrato natural universal074. Não modifica aquele contrato, não demonstra extensão dessas primitivas a mapas constantes e não as declara contratermos causalmente admissíveis. O objetivo físico geral permanece íntegro. A utilidade é tornar explícita a primitiva disponível no fundo físico e a obrigação exata de admissibilidade/transporte que ela ainda precisa satisfazer.

## 1. Entradas e novidade real

A {free}, §3, já contém o extrator diferencial local F, ali chamado ℰ, com FK=Id. Não reivindicamos a descoberta dessa identidade em088. A {bv} fornece a ação BV, o par não mínimo e a férmion que produz o gauge fixado usado na {causal}. A presente nota acrescenta a homotopia no complexo COMPLETO de jatos BV e sua extensão por todas as valências, com controle do diferencial horizontal.

Trabalhamos em M=(0,π)×S³, ḡ=dr²−a(r)²γ, a=2cos(r/2), φ̄=id. O fundo resolve as equações Einstein–sigma fixadas na linhagem. Testes têm suporte compacto interior. Hubble ℌ=a′/a=−½tan(r/2) não é a Hessiana ℋ. K(v)=(Lie_v ḡ,dφ̄(v)) é o operador de gauge linear e ℋK=K*ℋ=0 são identidades diferenciais exatas no fundo on-shell.

O parâmetro t que organiza valência não é r. Coeficientes herdados, se acrescentados, são uma álgebra real unital de ghost zero, inerte sob s. Não há fonte externa de ghost positivo nesta categoria. Em particular, fontes Ω de uma Ward adicional de comparação de fundos exigiriam outra análise; centralidade não as faz desaparecer.

## 2. Relógios naturais e a inversa já existente

Defina o escalar natural

    X(g,φ)=g^{μν}γ_ij(φ)∂_μφ^i ∂_νφ^j.

X̄=−3/a² e X̄′=6ℌ/a²=−3sin(r/2)/(4cos³(r/2))≠0 no interior. A primeira variação, para φ=Exp_φ̄(tξ), é

    δX=−a⁻⁴ γ^{ij}h_ij−2a⁻² div_γ ξ.

Ela é global porque ξ é seção de φ̄*TS³ e a divergência usa γ. Por naturalidade ativa de X e invariância do fundo sob s₀,

    s₀ξ=dφ̄(C),     s₀δX=dX̄(C).

O mapa de fibrados E(v)=(dφ̄(v),dX̄(v)) leva TM a φ̄*TS³⊕R e é invertível. Ponha ζ=F(h,ξ)=E⁻¹(ξ,δX). Na apresentação produto:

    ζ^i=ξ^i,
    ζ^r=δX/X̄′=[−a⁻²γ^{ij}h_ij−2div_γξ]/(6ℌ).

É exatamente o extrator068. Logo FK=Id e s₀ζ=C. Não se usa Green, inversa espacial de Laplaciano, equação de movimento de h/ξ ou coordenadas globais escalares do alvo.

A escrita intrínseca da inversa pode ser dada num aberto de jatos que contém este fundo. Escreva A=dφ̄ e A†=ḡ⁻¹ A*γ. Se B=AA† é invertível, U=A†B⁻¹ satisfaz AU=Id. P=Id−UA projeta em ker A. Para η=dX̄ e d=η(Pη♯)≠0,

    E⁻¹(w,z)=Uw+Pη♯(z−η(Uw))/d.

Aplicar A dá w; aplicar η dá z. Todos os objetos transportam seus fibrados naturalmente. No fundo físico B=−a⁻²Id, η=X̄′dr, d=(X̄′)². Esta fórmula define um aberto suficiente, não afirma que B invertível seja necessário para toda inversa possível de E. Denominadores são suaves e não nulos sobre cada compacto interior. Famílias que cheguem ao conjunto degenerado ficam fora dessa localização.

## 3. Coordenadas de jatos realmente independentes

Defina o tensor

    H=h−Lie_ζ ḡ.

Pela primeira componente de Eζ=(ξ,δX), ξ−dφ̄ζ=0. Pela segunda, a variação de X na parcela (H,0) é zero. Equivalentemente,

    τ(H)=ḡ^{μα}ḡ^{νβ}(φ̄*γ)_αβ H_μν=0.

No fundo produto isso é γ^{ij}H_ij=0. H é seção de ker τ⊂Sym²T*M, um fibrado de posto nove. Não há dez componentes independentes de H. Sua decomposição por direção temporal e espacial tem postos1+3+5.

A transformação tem inversa diferencial explícita

    (H,ζ) ↦ (h,ξ)=(H+Lie_ζḡ,dφ̄ζ),    τ(H)=0.

De fato F(H,0)=0 e FKζ=ζ. Portanto ambas as composições são identidade em seções e após todos os prolongamentos. A mudança usa ordem no máximo dois na direção (h,ξ)→(H,ζ) e ordem no máximo um na inversa. Isso é um isomorfismo das álgebras de funções de FINITOS jatos, no limite direto sobre a ordem; não é um isomorfismo entre J^k dos dois sistemas para o mesmo k.

Podem-se usar coordenadas locais independentes do fibrado ker τ, ou uma conexão projetada nesse fibrado. Suas relações de prolongamento são preservadas. ζ e C são seções do mesmo fibrado TM, de paridades opostas. A mudança é linear nas variáveis dinâmicas e conserva valência. Por FK=Id,

    s₀H=0,     s₀ζ=C,     s₀C=0.

## 4. Por que os antifields não invalidam o doublet

Primeiro desfaça a transformação canônica gerada pela férmion de gauge069, Ψ=−⟨barC,Ch−b/(2ℓ)⟩. É uma translação dos antifields pelas derivadas variacionais de Ψ, de ordem diferencial finita, com inversa de sinal oposto. Ψ é quadrática e a transformação conserva valência. Não se elimina b usando sua equação; conserva-se o setor não mínimo off-shell. A conjugação transporta cohomologia e formas locais, pois a mudança é prolongada por derivadas totais.

Na apresentação não fixada, a ação quadrática tem a forma

    S₂=½⟨u,ℋu⟩+⟨u*,KC⟩−⟨barC*,b⟩,     u=(h,ξ).

Os sinais de s₀ nos antifields são os determinados pelo antibracket069. Para a homotopia importa sua dependência, e ela é explícita:

    s₀u* = ±ℋu = ±ℋ(H,0),
    s₀C* = ±K*u*,
    s₀barC = −b,      s₀b=0,
    s₀b* = ±barC*,    s₀barC*=0.

Cada ± é o sinal fixo da apresentação canônica, não um parâmetro a escolher na prova. O argumento abaixo vale para qualquer desses sinais coerentes porque κ anula os dois lados dessas quatro linhas. A igualdade ℋu=ℋ(H,0) usa u=(H,0)+Kζ e ℋK=0 COMO IDENTIDADE DIFERENCIAL. Não se toma um quociente por integração por partes dos cociclos para apagar uma dependência real.

Podemos conservar os antifields antigos não fixados como coordenadas independentes ao fazer a mudança (h,ξ)↔(H,ζ). Essa mudança conjunta é invertível na álgebra de jatos e basta para a comparação de complexos; não a apresentamos como um lift canônico omitido dos antifields. O antibracket já fixou s₀ antes dessa mudança de coordenadas.

Os s₀-transformados dos geradores restantes não envolvem ζ,C nem seus jatos. Seus ghosts são:

    H:0; u*:−1; C*:−2; barC:−1; b:0; b*:−1; barC*:0.

Portanto todos os geradores que restam após retirar ζ,C têm ghost não positivo. Não é preciso demonstrar aciclicidade Koszul–Tate de ℋ(H,0), ausência de vínculos ou invertibilidade da Hessiana reduzida para a conclusão de ghost POSITIVO abaixo.

## 5. Homotopia no complexo completo e no diferencial horizontal

Defina uma derivação ímpar κ de ghost−1, sobre os jatos independentes, por

    κ(D_I C)=D_I ζ,     κ(D_I ζ)=0,
    κ(qualquer outro gerador)=0,

e κ=0 nos coeficientes de fundo. A definição é por prolongamento: κ comuta com cada derivada total de coeficientes. As fórmulas são globais sob mudança de frame de TM porque ζ e C transformam pelo mesmo mapa de fundo. Não se requer trivialização global de S³.

Se N conta os fatores ζ,C e seus derivados, as identidades nos geradores e a regra de Leibniz dão

    s₀κ+κs₀=N,     [N,s₀]=0.

Para formas locais, estenda κ(dx^μ)=0 com o sinal total graduado. Então

    κd_H+d_Hκ=0,     [N,d_H]=0.

Isso NÃO congela os jatos de fundo sob d_H: a derivada horizontal continua derivando os coeficientes e denominadores. A comutação resulta do prolongamento da derivação vertical κ. É um mecanismo distinto da normalização por coordenadas normais074, que não comutava com d_H.

Se π põe todos os jatos ζ,C a zero, defina h₀=κ/N nos monômios de N>0 e h₀=0 em N=0. N é um inteiro positivo e sua divisão é legítima sobre os reais e qualquer extensão escalar real. Por valência fixada só há finitos graus N. Obtêm-se as identidades exatas

    s₀h₀+h₀s₀=Id−π,
    (s₀+d_H)h₀+h₀(s₀+d_H)=Id−π.                    (1)

π pode deixar um complexo residual não trivial, mas esse complexo não tem gerador de ghost positivo e tem forma no máximo quatro. Consequentemente:

    H^g(s₀;formas de qualquer grau)=0 para g>0,
    H^n(s₀+d_H)=0 para grau total n>4.               (2)

A prova é direta: um ciclo A nesses graus tem πA=0; por (1), A=s₀h₀A ou A=(s₀+d_H)h₀A. A igualdade não requer uma primitiva que omita antifields. Este é o mecanismo de pares contráteis aplicado ao extrator físico: o procedimento padrão e seus pressupostos estão em [BBH, §2.7](https://arxiv.org/pdf/hep-th/0002245v3). A verificação dos pressupostos físicos, a mudança de jatos e a aplicação (1–2) são as etapas demonstradas aqui.

## 6. Todas as valências: recorrência explícita, sem convergência presumida

Use a álgebra completada por valência Ĉ_loc=∏_(E≥0) A_E, com finitos jatos e grau polinomial finito em cada coeficiente. Coeficientes de fundo pertencem à localização acima. Escreva

    s=s₀+s₊,     s₊=s₁+s₂+⋯,

onde s_j aumenta valência em j e ghost em um. O fundo on-shell remove o termo constante de s nos antifields. A ação069, expandida por Exp no pullback, fornece esta estrutura sem truncar arbitrariamente a interação. Cada coeficiente de uma composição recebe somente finitíssimas parcelas.

Se sA=0 e gh(A)>0, construa B por indução em E. Supondo escolhido B_<E de modo que R=A−sB_<E não tenha termos de valência menor que E, a identidade sR=0 implica s₀R_E=0. Por (1), tome

    B_E=h₀R_E.                                      (3)

Subtrair sB_E mata R_E e somente altera valências superiores. Iterar define a série formal B com sB=A coeficiente a coeficiente. h₀ conserva valência e s₊ a aumenta, de modo que a construção é contínua na topologia formal. Para cada E há finitamente muitas operações diferenciais, logo os jatos de B_E continuam finitos. Não se supõe uma cota uniforme de ordem sobre toda a série, nem convergência em t numérico.

A mesma prova vale para D=s+d_H=D₀+s₊, D₀=s₀+d_H, em qualquer grau total n>4. D₀ preserva valência; s₊ a aumenta. Se DΩ=0, a recorrência

    T_E=h₀(Ω−D T_<E)_E                              (4)

produz DT=Ω. Assim, na categoria localizada explicitada,

    H^g(Ĉ_loc,s)=0  (g>0),
    H^n(Ĉ_loc de formas,s+d_H)=0  (n>4).             (5)

Não se troca cohomologia com limite inverso para obter (5). A primitiva é construída por (3–4). A reconstrução torna (5) uma afirmação no BRST CLÁSSICO completo formal, não apenas na página de s₀. O operador quântico de Ward renormalizado não é s.

## 7. Aplicação exata, ainda condicionada, à quebra local

Se a primeira quebra consistente de Q2 admitir a descida completa Ω de grau total cinco na categoria de {descent}, sua imagem na localização satisfaz DΩ=0. A fórmula (4) então fornece uma primitiva T de grau total quatro. Seu componente de forma quatro tem ghost zero, e a equação de forma quatro diz

    aⁱ_4 = s T⁰_4 + d_H T¹_3.                      (6)

O expoente i aqui é ghost um (a¹_4); todos os índices são ghost/forma, não valências ou laços. A expressão (6) é uma exatidão clássica FORMAL na localização. Se a descida ainda não pertence a essa completação, sua inclusão/comparação continua hipótese; não se elimina a obrigação por chamar ambos os espaços de locais.

A fórmula é local e preserva suporte: mudanças de jatos, h₀ e os diferenciais usam somente derivadas e coeficientes no mesmo ponto. São reais quando os dados e o cociclo são reais. h₀ conserva a valência, de modo que conserva o peso t^(E+2L−2) a laço L fixo antes das correções de valências superiores organizadas na mesma série. Isso é controle ALGÉBRICO Rees; não é uma prova das cotas transversais de escala ou da hierarquia de inserções da {norm}.

Permanecem a extensão dos coeficientes para a classe universal sem inversas proibidas, regularidade exigida pelas normalizações, as cotas de escala da aplicação multilinear inteira, EOM/contatos, realidade das convenções completas e compatibilidade entre aridades e ordens. Não se afirma QME a partir de (6), nem estado positivo interagente ou independência entre fundos.

## 8. A localização não pode ser apagada do enunciado

A {nat}, §1, exige expressamente ausência de inversões que eliminem mapas constantes e os jatos simétricos usados como controle. Aqui A=dφ̄=0 em mapa constante torna E não invertível. Mesmo na família produto, o extrator usa 1/ℌ, singular quando a′=0. Os extremos r=0 e a=0 não pertencem ao fundo físico considerado; sua exclusão não demonstra extensão a outras referências admitidas pelo contrato universal.

Há um controle matemático adicional. A {h4}, com seu {h4review}, constrói uma classe A_I não nula em ghost quatro no setor de espaço-forma/sigma constante projetado. Se existisse uma homotopia UNIVERSAL, compatível com essa projeção de complexos, que satisfizesse a identidade contratante positiva de (1) também naquele setor, aplicada ao ciclo A_I ela o tornaria fronteira. Isso contradiz o detector em C₆ da087. Portanto uma tal extensão da homotopia, com essas propriedades simultâneas, não existe.

Esse controle não demonstra uma anomalia física de ghost um nem impede uma primitiva universal apenas para a quebra concreta de grau total cinco. Também não prova que todo termo de uma primitiva localizada tenha um polo inevitável; cancelamentos podem ocorrer para cociclos específicos e precisam ser medidos. O que fica decidido é que não se pode promover (5) inteiro ao contrato universal omitindo sua localização.

## 9. Alcance e próxima obrigação

[DERIVED — pendente de revisão] A identidade de gauge068 foi estendida a uma homotopia local no BV completo e a primitivas formais em todas as valências no aberto de relógios físicos. Isso desloca a próxima ação para verificar a admissibilidade/possível cancelamento de denominadores da primitiva de uma quebra concreta, ou continuar a prova diretamente no contrato universal. Não substitui o objetivo geral por suficiência numa subcategoria.

[OPEN] Normalização causal/QME na classe efetiva, estado e observáveis físicos interagentes, comparação de fundos, reconstrução geral pelos mesmos dados e UV. Fase/ramo e H3 interno já pagos não são reabertos.

[REAL — documentação] Fontes medidas antes/depois; somente esta nota, o manifesto e o helper novos sob Chatgpt. Nenhum original, Atlas, índice, memória canônica, um.py ou artefato selado foi alterado. Zero execução matemática/CAS/Lean/um/natureza. A {prior} é antecedente concluído; revisões088 serão ligadas por adendo novo, nunca atribuídas antes de sua emissão.
'''
labels={'free':'nota BRST livre068','bv':'ação BV069','causal':'construção causal069','norm':'admissibilidade072','nat':'classe natural074','descent':'descida075','rees':'completação Rees074','h4':'classe par087','h4review':'parecer independente087','prior':'entrega087'}
for k in sources:
    body=body.replace('{'+k+'}',L(k,labels[k]))
body=body.replace('aⁱ_4','a¹_4').replace('O expoente i aqui é ghost um (a¹_4);','O expoente de a¹_4 é ghost um;')

def new(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp=path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    tmp.rename(path)
    assert path.read_bytes()==raw

checks=[]
for p in pins:
    raw=Path(p['path']).read_bytes()
    ok=len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256']
    assert ok; checks.append({'name':p['path'],'passed':ok})
for p in re.findall(r'\]\(<(C:/[^>]+)>\)',body):
    assert Path(p).is_file(); checks.append({'name':'link:'+p,'passed':True})
new(OUT/'PRIMITIVAS_BV_FORMAIS_NO_ABERTO_DOS_RELOGIOS.md',body.encode('utf-8'))
new(OUT/'MANIFESTO_HOMOTOPIA_BV_088.json',(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'status':'WRITTEN_DERIVATION_PENDING_INDEPENDENT_REVIEW__LOCALIZED_CATEGORY_ONLY','pins':pins,'checks':checks,'checks_total':len(checks),'checks_passed':len(checks),'new_mathematics_executed':0,'new_lean_compilations':0,'originals_written':False,'um_executed_or_imported':False,'qme_claimed':False,'universal_category_replaced':False},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'path':(OUT/'PRIMITIVAS_BV_FORMAIS_NO_ABERTO_DOS_RELOGIOS.md').as_posix(),'bytes':len(body.encode('utf-8')),'documentary_checks':len(checks)}))
