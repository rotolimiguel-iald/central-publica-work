from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REVISOES_RAIZ_087_20260910'
assert not OUT.exists()
OUT.mkdir()
paths = {
 'n1':'CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md',
 'n2':'COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md',
 'r1':'REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md',
 'r2':'REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md',
 'class':'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
 'rc':'REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md',
 'ad':'REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md',
 'criterion':'CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md'
}
pins = []
for path in paths.values():
    p = ROOT / path; raw = p.read_bytes()
    pins.append({'path':p.as_posix(), 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})

def link(label, key):
    return '['+label+'](<'+(ROOT/paths[key]).as_posix()+'>)'

text = '''# Revisão da raiz087 — setores CE e alcance da composição clássica

10/09/2026. /root. [DERIVED — revisão escrita]. [REAL — integridade documental, separada da matemática].

Li integralmente as demonstrações dos setores linear e quadrático na preparação desta entrega e, após sua emissão, os dois pareceres independentes específicos. Não identifiquei erro material no contrato comum: espaço-forma Lorentziana orientada de dimensão quatro, K>0 fixo, setor métrico com sigma constante projetado, coeficientes reais herdados inertes e finitos jatos em cada elemento. A conclusão não é uma compilação Lean nem um cálculo executado.

## 1. Setor linear

{n1}

O ponto decisivo é a ausência de tipos de formas exteriores no módulo graduado de Weyl: os pesos (r+4,r) e (r,r+4) têm diferença quatro, enquanto ΛᵖV* exige diferença zero ou dois. A injeção estrita no símbolo plano transporta essa ausência ao quociente curvo, pois um elemento não nulo de ordem finita tem símbolo principal não nulo. Logo Bᵖ(N₁)=0 para p=0,…,4.

Esse resultado horizontal sozinho não seria uma prova de aciclicidade do CE inteiro. A nota paga a etapa adicional: cada corte finito sob a isotropia semissimples tem coeficientes sem componente trivial; a cohomologia vertical é zero em todos os graus. Cissões equivariantes finitas conservam primitivas invariantes. Elimina-se o menor grau horizontal subtraindo dR com o diferencial completo, incluindo curvatura. Há no máximo cinco valores horizontais. Em grau vertical zero, o ciclo já é zero; não se inventa uma primitiva de grau negativo.

Tensorizar os argumentos reais com Rher conserva exatidão, inclusive com nilpotentes. O resultado é HᵠCE(g,N₁)ʰ=0. Na filtração por valência isso é a aciclicidade de d₁ na diagonal m=E−ghost=1, e não a nulidade do espaço H(s₀) dessa diagonal. O {r1} conferiu também a hipótese finita da importação Chevalley–Eilenberg. Minha leitura do parecer não é apresentada como nova leitura direta da primária histórica.

## 2. Setor quadrático

{n2}

A prova constrói I_r=½⟨∇̄_(r)W,∇̄_(r)W⟩ e J_r=½⟨∇̄_(r)W,*∇̄_(r)W⟩ como elementos CURVOS efetivos, com simetrização normalizada. Os dois símbolos independentes fornecem geração e independência por redução finita da maior ordem. A filtração usa a SOMA das ordens dos fatores; K tem grau zero. Assim B⁰ tem base algébrica I_r,J_r, e B¹ tem base dI_r,dJ_r.

Para B², os tipos permitidos aparecem com sinal de troca negativo no produto de dois Weyl de mesma ordem. São excluídos da potência simétrica bosônica. Os tipos cruzados não atingem o alvo. Portanto B²=0. Essa etapa não foi inferida da classificação de vetores.

A igualdade □I_r=2I_(r+1)+L_r, e sua versão dual, tem restos de ordem no máximo 2r+4. Os comutadores curvos atuam em TODOS os índices, e ∇̄R₀=0 é usado explicitamente. A diagonal dois vem do termo de Leibniz e da simetrização normalizada. Permite redução finita a I₀,J₀ no quociente por □; a ordem principal impede uma relação residual não nula. Não se inverte □ e não se estende a jatos infinitos por coeficiente.

Segue Hᵖrel(N₂)=0 salvo p=4, onde há duas classes livres. No CE inteiro, a filtração horizontal tem cinco níveis e a segunda página só tem coluna p=4. Nenhum diferencial posterior entra ou sai. Os dois geradores verticais de grau três dão os postos 2,4,2 em graus totais 4,7,10, respectivamente. A coluna única em cada grau elimina extensões entre peças; não há limite inverso nesse cálculo.

O {r2} verifica separadamente esses passos e conserva a distinção entre a cohomologia CE após d₁ e o BRST clássico completo. I₀ usa a normalização da086: I082=2I₀; J₀ mantém a convenção. Não se mistura J₀, pseudoescalar, com o operador J=Luz.

## 3. Composição da classe par: autoria e revisão separadas

A {classlink} é de minha autoria. Não a apresento como aprovada independentemente por mim. Seu {rc} é de Herschel; o {ad} registra a leitura efetiva do parecer quadrático de Singer, fechando a dependência documental da composição sem misturar as autorias.

A conclusão revista é uma linha livre Rher[A_I] em H⁴(C_N,s) para N≥6 e no complexo formal, detectada pela projeção a C₆. s é o BV–BRST CLÁSSICO completo por valência. A impossibilidade de uma primitiva considera o complexo com antifields; não há hipótese de ausência de antifields para possíveis fronteiras. O ciclo completo de Pontryagin, por sua vez, tem a primitiva de transgressão e é s-exato. A diferença não é uma contradição: sua primitiva começa em valência inferior e liga diagonais distintas do CE.

Não se conclui que H⁴ inteiro seja uma linha, que todas as outras classes desapareçam, que um limite inverso comute com cohomologia, ou que s já seja um operador quântico renormalizado.

## 4. Efeito sobre o caminho crítico

A {criterion} foi lida integralmente. Suas remissões tornam explícito que o critério074 exige grupos de FORMAS com coeficientes em H(s) completo: em particular H¹(Ē;H⁴(s)), além dos outros canais de grau total cinco. Não exige simplesmente H⁴(s)=0. Portanto a linha par não refuta esse critério nem é, por si, uma anomalia física de ghost um.

A revisão matemática acima é dos setores CE. A auditoria074 terá exame independente próprio de suas condições; não conto minha leitura de seu texto como nova prova de todas as importações e normalizações causais ali catalogadas. Continua possível trabalhar diretamente com uma primitiva admissível da anomalia concreta, em vez de provar nulidade de cada grupo suficiente.

Ainda faltam o transporte ao setor físico sigma não constante, admissibilidade e compatibilidade dos contratermos, fechamento interagente/QME, a rota UV e a realização gravitacional dos MESMOS dados selecionados. A fase/ramo e H3 interno já pagos na linhagem não são reabertos pela homonímia com graus de cohomologia.

## 5. Custódia

Este emissor mediu os oito arquivos efetivamente referidos antes/depois e verificou os destinos dos links. Fonte lida e parecer lido são atividades distintas de execução matemática. Nenhum um.py, CAS, Lean ou rito foi executado; nenhum original, Atlas, índice ou memória canônica foi escrito. Somente esta nota nova, seu recibo e o helper novo vivem em Chatgpt.
'''.format(n1=link('Demonstração linear de Herschel.','n1'), n2=link('Demonstração quadrática de Turing.','n2'), r1=link('parecer de Turing','r1'), r2=link('parecer de Singer','r2'), classlink=link('nota da classe par','class'), rc=link('parecer independente','rc'), ad=link('adendo subsequente','ad'), criterion=link('auditoria do critério074 por Singer','criterion'))

def new(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp = path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw

checks = []
for p in pins:
    raw=Path(p['path']).read_bytes()
    ok=len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256']
    assert ok; checks.append({'name':p['path'], 'passed':ok})
for path in re.findall(r'\]\(<(C:/[^>]+)>\)',text):
    assert Path(path).is_file()
    checks.append({'name':'link:'+path, 'passed':True})
new(OUT/'PARECER_CE_LINEAR_QUADRATICO_E_ALCANCE_087.md',text.encode('utf-8'))
new(OUT/'REGISTRO_REVISAO_RAIZ_087.json',(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(), 'pins':pins,'checks':checks, 'checks_total':len(checks),'checks_passed':len(checks),'mathematics_executed':False,'lean_executed':False,'um_executed_or_imported':False,'originals_written':False,'own_full_h4_source_not_self_approved':True},ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'folder':OUT.as_posix(),'documentary_checks':len(checks),'mathematics_executed':False}))
